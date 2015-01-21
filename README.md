# django_zoneadmin
Alternative admin interface for Django using Bootstrap.

## Installing

Do a `pip install django_zoneadmin`. Once installed, open your settings.py file and place the 'zone_admin' app *before* the 'django.contrib.admin' app. You also need to include the 'widget_tweaks' app.

After that, do a `python manage.py collectstatic` to get the staticfiles and refresh the browser, you should now see that the styling of the admin interface has changed.
