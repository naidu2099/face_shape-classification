from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path
import os
import markdown

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def index(request):
    """
    Main landing page.
    Shows home page with options to login, register, or admin login.
    """
    return render(request, 'home.html')

@login_required(login_url='login')
def generate(request):
    """
    Generate face analysis (protected - login required).
    """
    if request.method == 'POST':
        if 'user_image' not in request.FILES:
            messages.error(request, "No photo uploaded.")
            return redirect('user_dashboard')

        file = request.FILES['user_image']
        if not file.name:
            messages.error(request, "No photo selected.")
            return redirect('user_dashboard')

        if file and allowed_file(file.name):
            # Create upload directory
            upload_folder = Path(settings.BASE_DIR) / 'static' / 'uploads'
            upload_folder.mkdir(parents=True, exist_ok=True)

            # Save file
            filename = file.name
            upload_path = upload_folder / filename
            with open(upload_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            user_gender = request.POST.get('user_gender', 'auto')
            return perform_generation(request, upload_path, user_gender)
        else:
            messages.error(request, 'Invalid file type.')
            return redirect('user_dashboard')

    return redirect('user_dashboard')

@login_required(login_url='login')
def perform_generation(request, upload_path, user_gender='auto'):
    """
    Perform face analysis generation (protected - login required).
    """
    from face_app.gemini_gen import generate_styles_and_tips

    # Create generated folder
    generated_folder = Path(settings.BASE_DIR) / 'static' / 'generated'
    generated_folder.mkdir(parents=True, exist_ok=True)

    # Generate styles
    gen_image, face_shape, tips, vision = generate_styles_and_tips(
        str(upload_path),
        str(generated_folder),
        user_gender=user_gender
    )

    # Convert Markdown to HTML
    formatted_tips = markdown.markdown(tips)
    formatted_vision = markdown.markdown(vision)

    # Ensure original image path is correct for template
    original_image_path = str(upload_path).replace('\\', '/')
    if 'static/' in original_image_path:
        original_image_path = original_image_path.split('static/')[-1]
    else:
        original_image_path = 'uploads/' + os.path.basename(str(upload_path))

    return render(request, 'face_app/results.html', {
        'original_image': original_image_path,
        'generated_image': gen_image,
        'face_shape': face_shape,
        'beauty_tips': formatted_tips,
        'style_vision': formatted_vision
    })

@login_required(login_url='login')
def regenerate(request):
    """
    Regenerate face analysis (protected - login required).
    """
    image_path = request.GET.get('image')
    if not image_path or not image_path.startswith('uploads/'):
        return redirect('user_dashboard')

    full_path = Path(settings.BASE_DIR) / 'static' / image_path
    if not full_path.exists():
        messages.error(request, "Original photo missing.")
        return redirect('user_dashboard')

    return perform_generation(request, full_path)
