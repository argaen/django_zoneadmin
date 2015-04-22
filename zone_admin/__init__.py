from django.conf import settings

import os
BASE_DIR = os.path.dirname(__file__)

default_path = os.path.join(BASE_DIR, 'templates/default')
if hasattr(settings, 'ZONEADMIN_THEME'):
    path = os.path.join(BASE_DIR, 'templates/', settings.ZONEADMIN_THEME)

    if settings.ZONEADMIN_THEME == 'bootstrap_dashboard':
        settings.TEMPLATE_DIRS += ((path, default_path) if os.path.isdir(path) else (default_path,))
    else:
        settings.TEMPLATE_DIRS += ((path,) if os.path.isdir(path) else (default_path,))
else:
    settings.TEMPLATE_DIRS += (default_path,)

settings.TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)
