from django.apps import AppConfig
from django.conf import settings

import os


class ZoneAdminConfig(AppConfig):

    name = 'zone_admin'

    def ready(self):

        # Configure TEMPLATE_DIRS variable to append theme dir according to ZONEADMIN_THEME variable
        base_dir = os.path.dirname(__file__)
        default_path = os.path.join(base_dir, 'templates/default')
        if hasattr(settings, 'ZONEADMIN_THEME'):
            path = os.path.join(base_dir, 'templates/', settings.ZONEADMIN_THEME)

            if settings.ZONEADMIN_THEME == 'bootstrap_dashboard':
                settings.TEMPLATE_DIRS += ((path, default_path) if os.path.isdir(path) else (default_path,))
            else:
                settings.TEMPLATE_DIRS += ((path,) if os.path.isdir(path) else (default_path,))
        else:
            settings.TEMPLATE_DIRS += (default_path,)

        # Add request to TEMPLATE_CONTEXT_PROCESSORS
        settings.TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)
