import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import CustomUser

def create_admin():
    username = 'mani'
    email = 'mani@example.com'
    password = 'Mani12@'
    full_name = 'Mani Administrator'
    
    user, created = CustomUser.objects.get_or_create(
        username=username, 
        defaults={'email': email, 'full_name': full_name}
    )
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    
    if created:
        print(f"Superuser {username} created successfully!")
    else:
        print(f"Superuser {username} updated successfully!")

if __name__ == '__main__':
    create_admin()

