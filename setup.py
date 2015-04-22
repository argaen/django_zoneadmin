from setuptools import setup

packages = ['Django']

setup(
    name="django_zoneadmin",
    version="0.3",
    url="http://github.com/argaen/django_zoneadmin",
    description="Alternative django administration interface with bootstrap",
    author="argaen",
    author_email="manu.mirandad@gmail.com",
    packages=['zone_admin'],
    include_package_data=True,
    keywords=['django', 'admin', 'bootstrap', 'djangozone'],
    install_requires=packages
)
