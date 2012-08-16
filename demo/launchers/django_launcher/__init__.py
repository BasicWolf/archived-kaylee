import os
from django.core import management

def run():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kl_django.settings")
    management.call_command('runserver', '5000')
