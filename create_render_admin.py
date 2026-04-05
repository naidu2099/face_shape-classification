import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

def create_admin():
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    if not CustomUser.objects.filter(username=username).exists():
        print(f"Creating superuser {username}...")
        CustomUser.objects.create_superuser(username, email, password)
        print("Superuser created successfully!")
    else:
        print(f"Superuser {username} already exists.")

if __name__ == '__main__':
    create_admin()
