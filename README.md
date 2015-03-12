# Django Zone Admin
Alternative admin interface for Django using Bootstrap.

## Installing

Do a `pip install django_zoneadmin`. Once installed, open your settings.py file and place the 'zone\_admin' app *before* the 'django.contrib.admin' app.

After that, (if you are in DEBUG=False mode) do a `python manage.py collectstatic` to get the staticfiles and refresh the browser, you should now see that the styling of the admin interface has changed.


## Tag fields

You can improve the tag field with [bootstrap tagsinput](http://timschlechter.github.io/bootstrap-tagsinput/examples/). In order to use it, in your admin file place the following:

```python
    from django.contrib import admin
    from django import forms

    from taggit.forms import TagWidget

    import models

    class ContentForm(forms.ModelForm):
        class Meta:
            model = models.Content
            widgets = {
                'tags': TagWidget(attrs={'data-role': 'tagsinput'}),
            }
            exclude = []

    class ContentAdmin(admin.ModelAdmin):
        form = ContentForm
```



This snippet, tells to use the tag widget for the field called **tags** of our **Content** model. Please, note that the example is integrating it with [django-taggit](https://github.com/alex/django-taggit). In case you just have a field with a comma separated list, do it with the following:


```python
    from django.contrib import admin
    from django import forms

    import models

    class ContentForm(forms.ModelForm):
        class Meta:
            model = models.Content
            widgets = {
                'tags': forms.TextInput(attrs={'data-role': 'tagsinput'}),
            }
            exclude = []


    class ContentAdmin(admin.ModelAdmin):
        form = ContentForm
```


## TinyMCE editor

If you want to have a textfield with the tinymce editor, do the following (customization of the editor is not posible yet):

```python
    from zone_admin.widgets import TinyMCEWidget

    class ContentForm(forms.ModelForm):

        class Meta:
            model = models.Content
            widgets = {
                'description': TinyMCEWidget(),
            }
            exclude = []

    class ContentAdmin(admin.ModelAdmin):
        form = ContentForm
```
