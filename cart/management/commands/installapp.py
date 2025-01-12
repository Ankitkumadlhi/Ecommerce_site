import os
import importlib
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Create a new app and add it to the installed apps'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The name of the app')

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        # Create the app
        self.create_app(app_name)
        # add the app to the installed apps
        self.add_to_installed_apps(app_name)
        
    
    def create_app(self, app_name):
        os.system(f'python manage.py startapp {app_name}')
        self.stdout.write(self.style.SUCCESS(f'Successfully created {app_name}'))
    
    def add_to_installed_apps(self, app_name):
        # add the app to the installed apps
        setting_module = os.environ.get('DJANGO_SETTINGS_MODULE')
        if not setting_module:
            self.stdout.write(self.style.ERROR('DJANGO_SETTINGS_MODULE is not set'))

        setting_file = importlib.import_module(setting_module)

        #construct the path to the settings file
        settings_path = os.path.dirname(setting_file.__file__)
        settings_file_path = os.path.join(settings_path, 'settings.py')
        # import the settings   

        with open(settings_file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if 'INSTALLED_APPS' in line:
                for j in range(i+1, len(lines)): 
                    if lines[j].strip() == ']':
                        lines.insert(j, f"    '{app_name}',\n")
                        break
                break
        with open(settings_file_path, 'w') as f:
            f.writelines(lines)

        self.stdout.write(self.style.SUCCESS(f'Successfully added {app_name} to installed apps'))


        # settings.INSTALLED_APPS.append(app_name)
        # # save the settings
        # with open('settings.py', 'w') as f:
        #     f.write(f'INSTALLED_APPS = {settings.INSTALLED_APPS}')
        # # import the app
        # importlib.import_module(app_name)
        # self.stdout.write(self.style.SUCCESS(f'Successfully installed {app_name}'))
        