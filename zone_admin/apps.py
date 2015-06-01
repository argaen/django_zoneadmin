from django.apps import AppConfig
from django.conf import settings

import os


class ZoneAdminConfig(AppConfig):

    name = 'zone_admin'

    def ready(self):

        # Configure TEMPLATE_DIRS variable to append theme dir according to ZONEADMIN_THEME variable
        base_dir = os.path.dirname(__file__)
        default_path = os.path.join(base_dir, 'templates/default')

        project_dir = settings.BASE_DIR
        project_default_path = os.path.join(project_dir, 'templates/default')
        project_theme_path = None
        template_dirs = []

        if hasattr(settings, 'ZONEADMIN_THEME'):
            theme_path = os.path.join(base_dir, 'templates/', settings.ZONEADMIN_THEME)
            project_theme_path = os.path.join(project_dir, 'templates/', settings.ZONEADMIN_THEME)

            if settings.ZONEADMIN_THEME == 'bootstrap_dashboard':
                template_dirs += [theme_path, default_path] if os.path.isdir(theme_path) else [default_path,]
            else:
                template_dirs += [theme_path,] if os.path.isdir(theme_path) else [default_path,]
        else:
            template_dirs += [default_path,]

        if os.path.isdir(project_default_path):
            template_dirs += [project_default_path] + template_dirs
        if project_theme_path is not None and os.path.isdir(project_theme_path):
            template_dirs += [project_theme_path] + template_dirs

        if hasattr(settings, "TEMPLATES"):
            for backend in settings.TEMPLATES:
                backend["DIRS"] = template_dirs + backend["DIRS"]
        else:
            settings.TEMPLATE_DIRS = [template_dirs] + settings.TEMPLATE_DIRS

        # Add request to TEMPLATE_CONTEXT_PROCESSORS
        settings.TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)
