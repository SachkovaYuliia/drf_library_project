import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_project.settings')

django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = "admin"
    password = "admin_password"
    email = "admin@gmail.com"

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email)
        print(f"Admin user '{username}' created successfully.")
    else:
        print(f"Admin user '{username}' already exists.")
from django.contrib.auth.models import User

user = User.objects.get(username='admin')

