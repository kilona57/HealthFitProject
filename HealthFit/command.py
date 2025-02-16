import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthfit.settings')
django.setup()

os.system('python manage.py makemigrations')
os.system('python manage.py migrate')
os.system('python scripts/import.py')
os.system('python manage.py runserver 0.0.0.0:8000')
