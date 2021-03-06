# Django Zone Admin
Alternative admin interfaces for Django admin.

Currently there are two different themes. One which is the `default` that is a rewrite of original Django admin templates but giving it a Bootstrap look. Second, called `bootstrap_dashboard` is an implementation of the admin by using the [bootstrap dashboard example](http://getbootstrap.com/examples/dashboard/), the content part of this theme is the same as the `default` theme.

## Installation

Do a `pip install django_zoneadmin`. Once installed, open your **settings.py** file and place the 'zone_admin' app **before** the `django.contrib.admin` app.

After that, (if you are in `DEBUG=False` mode) do a `python manage.py collectstatic` to get the _staticfiles_ and refresh the browser, you should now see that the styling of the admin interface has changed.


### Choosing a theme

The theme to be used is set according to the value of `ZONEADMIN_THEME` variable in your **settings.py** file. By default it uses the (guess what) `default` theme. Current themes are:

    - 'default'
    - 'bootstrap_dashboard'



## Features

There are some features implemented to enhance the look and experience for other users.

### Tag fields

You can improve tag fields with [bootstrap tagsinput](http://timschlechter.github.io/bootstrap-tagsinput/examples/). In order to use it, in your admin file place the following:

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


### Rick text editor

If you need a rich text editor. Just use the [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor) package


## Customization

### Overriding templates

This package respects the template inheritance that works by default in Django so, if you want to override the `change_form.html` template for a specific app, you can create the file under `app/templates/change_form.html`.

If you want to override a template for the whole project, create a `templates/theme_name` under your project root. There, if you want to override the `base_site.html` template, you can do it in normal Django way: create the `admin/base_site.html` and write your code in it. After refreshing you should see the new changes.

> As you may have noticed, you don't have to write the TEMPLATE_DIRS variable in your **settings.py** file because the package configures it automatically according to the theme being used. I.e. if you set to use the `default` theme, you can write your custom templates under `templates/default` directly.

### Block menu template (bootstrap_default theme)

This menu is defined in the `base.html` template. It automatically loads the registered applications and models in the admin (according to the current user permissions). You can override it in any template that inherits from `base.html` by writting the following:

```python
{% block menu %}
  My custom menu
{% endblock menu %}
```

The default menu contains the following:

```Django
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

> IMPORTANT: Note that if you want your overriden menu to appear in any _subpage_, you should override the block in the `base_site.html` template. If you override it in for example, your `index.html` template, the menu will only apply to templates extending that template (which may not be the desired behaviour).

One important thing to take into account is that, if you build a custom menu disabling some models/apps to be accessed, you are only hiding the urls to the user but **they can still be accessed!**. If you want to disable access to some models or apps, just change the permissions for the needed users/groups.

This package, provides a custom templatetag to generate more specific menus checking model permissions. Let's say you only want to have a menu with the **User** model on it. This can be achieved with:

```Django
{% get_model 'auth' 'user' as model %}
<div class="list-group-item">
  <a href="{{ model.admin_url }}"><i class="fa fa-user"></i> {{ model.name }}</a>
  <div class="pull-right">
    {% if model.add_url %}
    <span><a href="{{ model.add_url }}" title="{% trans 'Add' %}" class="model-action addlink"><i class="fa fa-plus"></i></a><span>
    {% endif %}
    {% if model.admin_url %}
      <span><a href="{{ model.admin_url }}" title="{% trans 'Change' %}" class="model-action changelink"><i class="fa fa-edit"></i></a><span>
    {% endif %}
  </div>
</div>
```

### Overriding index page (bootstrap_default theme)

The index page is left blank on purpose in order to override it. To do so, create an `index.html` template and place there whatever you want. Basically, you will want to override the `content` block which is the one that controls what is shown in the content part (the part besides the menu sidebar).


### Creating a new theme

If you need to create a new theme, this package may help you with it's templatetags and to show you how to do it with the templates. If you feel that the theme is good enough, consider a pull request to add it to the package itself. Themes are placed under `zone_admin/templates/theme_name`.

### Overriding styles

If you need to change the styles of a theme, write them in `static/admin/styles.css`. The file is automatically loaded in `base.html` template.

### Overriding bootstrap styles

All the themes use bootstrap (default style, not primary) for css styling. If you want to override the default values, you can use the [bootstrap customization page](http://getbootstrap.com/customize/). Once generated, place the file in `static/admin/vendor/bootstrap/bootstrap.min.css` and the boostrap style will be overriden.
