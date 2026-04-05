import os
import requests
import base64
import time
import re
import traceback
from pathlib import Path
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
REPLICATE_TOKEN = os.getenv("REPLICATE_API_TOKEN")
STABLE_HORDE_KEY = os.getenv("STABLE_HORDE_API_KEY")
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_TOKEN = os.getenv("OPENAI_API_KEY")

# User requested high-quality settings
SDXL_STEPS = 30
SDXL_GUIDANCE = 7.5
SDXL_RESOLUTION = 1024

def generate_styles_and_tips(image_path, output_folder, user_gender='auto'):
    """
    Unified Generation Engine (V5):
    Replicate -> DALL-E 3 (Premium) -> Stable Horde -> Pollinations -> HF
    """
    os.makedirs(output_folder, exist_ok=True)

    # Prepare Image
    with open(image_path, "rb") as f:
        raw = f.read()
    img_b64 = base64.b64encode(raw).decode("utf-8")
    
    mime_type = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    data_uri = f"data:{mime_type};base64,{img_b64}"

    # 1. Gemini Analysis
    detected_gender = user_gender
    face_shape = "Detected"
    gen_keywords = "professional hairstyle, designer glasses"
    style_vision = "A refined transformation."
    face_description = "A person" # For DALL-E fallback
    tips = "Enhance your face shape with a natural, healthy glow. Stay hydrated and use quality grooming products."
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        # Enhanced analysis for better styling
        prompt = """Analyze this face with extreme precision for a luxury styling transformation.
        1. Identify Gender (Male/Female).
        2. Determine Face Shape (Oval, Round, Square, Heart, Diamond, or Oblong).
        3. Provide a 'Description' (e.g. 'Person with dark hair').
        4. Provide 'Keywords' for Image Gen: Focus on ONE specific bold HAIRSTYLE and ONE specific stylish EYEWEAR (glasses).
        5. Provide 'Vision': A brief, inspiring 1-sentence style goal.
        6. Provide 'Tips': 3 bullet points of beauty/grooming advice for this specific face shape.
        
        Return STRICTLY in this format:
        Gender: [Gen]
        Shape: [Shape]
        Description: [Desc]
        Keywords: [Hair and Glasses]
        Vision: [Style vision]
        Tips: [Bullet point tips]"""

        payload = {
            "contents": [{"parts": [{"text": prompt}, {"inline_data": {"mime_type": mime_type, "data": img_b64}}]}]
        }
        resp_raw = requests.post(url, json=payload, timeout=20)
        if resp_raw.status_code == 200:
            resp = resp_raw.json()
            if "candidates" in resp and resp["candidates"]:
                full_text = resp["candidates"][0]["content"]["parts"][0]["text"]
                
                gen_match = re.search(r"Gender:\s*(.*)", full_text, re.IGNORECASE)
                shape_match = re.search(r"Shape:\s*(.*)", full_text, re.IGNORECASE)
                desc_match = re.search(r"Description:\s*(.*)", full_text, re.IGNORECASE)
                keywords_match = re.search(r"Keywords:\s*(.*)", full_text, re.IGNORECASE)
                vision_match = re.search(r"Vision:\s*(.*)", full_text, re.IGNORECASE)
                tips_match = re.search(r"Tips:\s*([\s\S]*)", full_text, re.IGNORECASE)

                face_description = desc_match.group(1).strip() if desc_match else "A person"
                face_shape = shape_match.group(1).strip() if shape_match else "Detected"
                gen_keywords = keywords_match.group(1).strip() if keywords_match else "luxury hairstyle, designer glasses"
                style_vision = vision_match.group(1).strip() if vision_match else "Transformation based on your unique features."
                tips_content = tips_match.group(1).strip() if tips_match else "Use high-quality products for a better look."

                if user_gender and user_gender.lower() != 'auto':
                    detected_gender = user_gender
                else:
                    detected_gender = gen_match.group(1).strip() if gen_match else "person"
                
                # Combine vision and tips for the UI
                style_vision = style_vision
                tips = tips_content
    except Exception as e:
        print(f"Gemini Error: {e}")
        detected_gender = user_gender if user_gender.lower() != 'auto' else "person"
        tips = "Focus on moisturizing and proper grooming."

    # 2. Build Prompts
    extra_realism = "photorealistic studio portrait, 8k, highly detailed, raw photo"
    neg_prompt = "anime, cartoon, CGI, 3d, illustration, glasses-free, original hair, blurry"
    
    # Positive prompt for style
    style_prompt = f"wearing NEW {gen_keywords}, {extra_realism}"
    final_prompt = f"{detected_gender} {style_prompt}, maintaining facial features, high quality photography."

    # 3. Generation Logic
    output_filename = f"styled_{int(time.time())}.jpg"
    output_path = os.path.join(output_folder, output_filename)
    success = False

    def is_valid_image(data):
        return data and len(data) > 10000

    # Pathway A: Replicate (InstantID)
    if REPLICATE_TOKEN:
        print("Path A: Replicate...")
        payload = {
            "version": "0825b094034822230780242af049755452d790d979857d474932371e42823632",
            "input": {
                "image": data_uri, "face_image": data_uri,
                "prompt": final_prompt, "negative_prompt": neg_prompt,
                "ip_adapter_scale": 0.8, "controlnet_conditioning_scale": 0.8,
                "num_inference_steps": SDXL_STEPS, "guidance_scale": SDXL_GUIDANCE,
                "width": SDXL_RESOLUTION, "height": SDXL_RESOLUTION
            }
        }
        try:
            h = {"Authorization": f"Token {REPLICATE_TOKEN}", "Content-Type": "application/json"}
            r_resp = requests.post("https://api.replicate.com/v1/predictions", json=payload, headers=h, timeout=25)
            if r_resp.status_code == 201:
                predict_id = r_resp.json()["id"]
                for _ in range(40):
                    time.sleep(3)
                    p_resp = requests.get(f"https://api.replicate.com/v1/predictions/{predict_id}", headers=h).json()
                    if p_resp.get("status") == "succeeded":
                        img_data = requests.get(p_resp["output"][0]).content
                        if is_valid_image(img_data):
                            with open(output_path, "wb") as f: f.write(img_data); success = True; break
        except Exception: traceback.print_exc()

    # Pathway B: DALL-E 3 (Premium Fallback)
    if not success and OPENAI_TOKEN:
        print("Path B: DALL-E 3...")
        # DALL-E 3 is T2I but amazing at logic. We use Gemini's description for identity.
        dalle_prompt = f"A photo of {face_description} with a NEW {gen_keywords}. Photorealistic studio portrait, high quality."
        try:
            h = {"Authorization": f"Bearer {OPENAI_TOKEN}", "Content-Type": "application/json"}
            p_payload = {"model": "dall-e-3", "prompt": dalle_prompt, "n": 1, "size": "1024x1024", "quality": "standard"}
            o_resp = requests.post("https://api.openai.com/v1/images/generations", json=p_payload, headers=h, timeout=60)
            if o_resp.status_code == 200:
                img_url = o_resp.json()["data"][0]["url"]
                img_data = requests.get(img_url).content
                if is_valid_image(img_data):
                    with open(output_path, "wb") as f: f.write(img_data); success = True
        except Exception: traceback.print_exc()

    # Pathway C: Stable Horde (Img2Img)
    if not success:
        print("Path C: Stable Horde...")
        h_url = "https://stablehorde.net/api/v2/generate/async"
        h_headers = {"apikey": STABLE_HORDE_KEY or "0000000000"}
        h_payload = {
            "prompt": final_prompt + " ### " + neg_prompt,
            "params": {"steps": 25, "denoising_strength": 0.85, "width": 1024, "height": 1024},
            "models": ["AbsoluteReality", "Realistic Vision V5.1", "AlbedoBase XL"]
        }
        if img_b64: h_payload["source_image"] = img_b64; h_payload["source_processing"] = "img2img"
        try:
            h_resp = requests.post(h_url, headers=h_headers, json=h_payload, timeout=20)
            if h_resp.status_code == 202:
                req_id = h_resp.json()["id"]
                for _ in range(30):
                    time.sleep(4)
                    c_resp = requests.get(f"https://stablehorde.net/api/v2/generate/status/{req_id}").json()
                    if c_resp.get("done"):
                        img_raw = c_resp["generations"][0]["img"]
                        img_data = requests.get(img_raw).content if img_raw.startswith("http") else base64.b64decode(img_raw)
                        if is_valid_image(img_data):
                            with open(output_path, "wb") as f: f.write(img_data); success = True; break
        except Exception: traceback.print_exc()

    # Pathway D: Hugging Face (Final Free fallback)
    if not success and HF_TOKEN:
        print("Path D: Hugging Face...")
        hf_url = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
        hf_headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        hf_payload = {"inputs": final_prompt}
        try:
            hf_resp = requests.post(hf_url, headers=hf_headers, json=hf_payload, timeout=60)
            if hf_resp.status_code == 200 and is_valid_image(hf_resp.content):
                with open(output_path, "wb") as f: f.write(hf_resp.content); success = True
        except Exception: traceback.print_exc()

    if success:
        return "generated/" + output_filename, face_shape, tips, style_vision
    else:
        return "uploads/" + os.path.basename(image_path), face_shape, "Analysis Fallback", "All pathways busy. Propping original."