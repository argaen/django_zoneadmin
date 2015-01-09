from setuptools import setup, find_packages

packages = ['Django', 'django-widget-tweaks', ]

setup(
    name="django_zoneadmin",
    version="0.1.1",
    url="http://github.com/argaen/django_zoneadmin",
    description="Alternative django administration interface with bootstrap",
    author="argaen",
    author_email="manu.mirandad@gmail.com",
    packages=['zone_admin'],
    keywords=['django', 'admin', 'bootstrap', 'angularjs'],
)
