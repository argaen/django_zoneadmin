# Django Zone Admin
Alternative admin interface for Django using Bootstrap.

## Installing

Do a `pip install django_zoneadmin`. Once installed, open your settings.py file and place the 'zone\_admin' app *before* the 'django.contrib.admin' app.

After that, (if you are in DEBUG=False mode) do a `python manage.py collectstatic` to get the staticfiles and refresh the browser, you should now see that the styling of the admin interface has changed.

You will also need to add the following line into your `TEMPLATE_CONTEXT_PROCESSORS` defined in your **settings.py** file: `django.core.context_processors.request`.




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


## Overriding templates

### Block menu

This menu is defined in the `base.html` template. It automatically loads the registered applications and models in the admin (according to the current user permissions). You can override it in any template that inherits from `base.html` by writting the following:

```python
{% block menu %}
  My custom menu
{% endblock menu %}
```

The default menu contains the following:

```python
{% load zoneadmin_utils %} # Needed for the get_app_list template tag
{% if user.is_authenticated %}
<div id="mainmenu" class="col-sm-3 col-md-2 sidebar" style="padding:0px;">
  <div class="list-group">
    {% get_app_list as app_list %}
    {% for app in app_list %}
      <a href="#{{ app.name | slugify }}" class="list-group-item" data-toggle="collapse" data-parent="#mainmenu">{{ app.name }}</a>
      <div class="collapse" id="{{ app.name | slugify }}">
        {% for model in app.models %}
        <div class="list-group-item sublist-group-item">
          <a href="{{ model.admin_url }}">{{ model.name }}</a>
          <div class="pull-right">
            {% if model.add_url %}
            <span><a href="{{ model.add_url }}" title="{% trans 'Add' %}" class="model-action addlink"><i class="fa fa-plus"></i></a><span>
            {% endif %}
            {% if model.admin_url %}
              <span><a href="{{ model.admin_url }}" title="{% trans 'Change' %}" class="model-action changelink"><i class="fa fa-edit"></i></a><span>
            {% endif %}
          </div>
        </div>
        {% endfor %}
      </div>
    {% endfor %}
  </div>
</div>
{% endif %}
```

### Overriding index page

The index page is left blank on purpose in order to override it. To do so, create an `index.html` template and place there whatever you want. Basically, you will want to override the `content` block which is the one that controls what is shown in the content part (the part besides the menu sidebar).
