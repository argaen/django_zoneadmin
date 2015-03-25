from django import template
from django.conf import settings
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.urlresolvers import reverse, NoReverseMatch
from django import forms
from django.template.loader import get_template
from django.template import Context
from django.forms.fields import TimeField, SplitDateTimeField
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils import six
from django.utils.text import capfirst
from django.apps import apps


register = template.Library()


class BootstrapWidgetNode(template.Node):
    def __init__(self, field_name, extra_attributes):
        self.extra_attributes = extra_attributes
        if 'is_inlines' in extra_attributes:
            self.is_inlines = extra_attributes.pop('is_inlines') == 'True'
        else:
            self.is_inlines = False
        self.field_name = field_name
        self.field = template.Variable(field_name)

    def render(self, context):
        try:
            actual_field = self.field.resolve(context)
            extra_attributes = dict(self.extra_attributes)

            if isinstance(actual_field.field, ReadOnlyPasswordHashField):
                return self.render_readonly_widgets(actual_field)

            if isinstance(actual_field.field, SplitDateTimeField):
                return self.render_date_time_widgets(actual_field)

            if isinstance(actual_field.field, forms.ModelMultipleChoiceField):
                return self.render_model_multiple_choice_widgets(actual_field)

            if isinstance(actual_field.field, forms.ModelChoiceField):
                return self.render_model_choice_widgets(actual_field)

            if isinstance(actual_field.field, forms.DateField):
                return self.render_date_widgets(actual_field)

            if isinstance(actual_field.field, TimeField):
                return self.render_time_widgets(actual_field)

            if isinstance(actual_field.field, forms.BooleanField) and not actual_field.is_hidden:
                return self.render_checkbox_widgets(actual_field)

            if isinstance(actual_field.field, forms.ImageField):
                return self.render_file_widgets(actual_field, image=True)
            elif isinstance(actual_field.field, forms.FileField):
                return self.render_file_widgets(actual_field)

            if hasattr(actual_field.field.widget, 'widgets'):
                pass

            if 'class' in actual_field.field.widget.attrs:
                extra_attributes['class'] = 'form-control {}'.format(actual_field.field.widget.attrs['class'])
            if actual_field.field.required and not self.is_inlines:
                extra_attributes['required'] = ''
            return actual_field.as_widget(attrs=extra_attributes)
        except template.VariableDoesNotExist:
            return ''

    def render_file_widgets(self, field, image=False):
        output = get_template('admin/widgets/file_widget.html')
        html_output = output.render(Context({
            'id': field.auto_id,
            'name': field.html_name,
            'value': field.value(),
            'media': settings.MEDIA_URL,
            'image': image,
            'required': field.field.required,
        }))
        return html_output

    def render_checkbox_widgets(self, field):
        output = get_template('admin/widgets/checkbox_widget.html')
        html_output = output.render(Context({
            'id': field.auto_id,
            'name': field.html_name,
            'value': "checked" if field.value() else "",
        }))
        return html_output

    def render_date_time_widgets(self, field):
        date_widget = field.field.widget.widgets[0]
        date_widget.attrs['class'] = 'date-field form-control'
        time_widget = field.field.widget.widgets[1]
        time_widget.attrs['class'] = 'time-field form-control'
        time_widget.attrs['size'] = 10
        values = field.value()
        if not isinstance(values, list):
            values = field.field.widget.decompress(field.value())
        output = get_template('admin/widgets/date_time_widget.html')
        html_output = output.render(Context({
            'date_widget': date_widget.render('{}_0'.format(field.html_name), values[0]),
            'time_widget': time_widget.render('{}_1'.format(field.html_name), values[1]),
        }))
        return html_output

    def render_date_widgets(self, field):
        date_widget = field.field.widget
        date_widget.attrs['class'] = 'date-field form-control'
        value = field.value()
        output = get_template('admin/widgets/date_widget.html')
        html_output = output.render(Context({
            'date_widget': date_widget.render(field.html_name, value),
        }))
        return html_output

    def render_time_widgets(self, field):
        time_widget = field.field.widget
        time_widget.attrs['class'] = 'time-field form-control'
        value = field.value()
        output = get_template('admin/widgets/time_widget.html')
        html_output = output.render(Context({
            'time_widget': time_widget.render(field.html_name, value),
        }))
        return html_output

    def render_model_choice_widgets(self, field):
        widget = field.field.widget
        can_add_related = False
        if hasattr(field.field.widget, 'widget'):
            widget = field.field.widget.widget
        else:
            field.field.widget.attrs['class'] = 'form-control'
            return field.as_widget()
        if hasattr(field.field.widget, 'can_add_related'):
            can_add_related = field.field.widget.can_add_related
        add_url = edit_url = None
        rel_to = field.field.widget.rel.to
        info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
        if can_add_related:
            add_url = reverse('admin:%s_%s_add' % info, current_app=field.field.widget.admin_site.name)
        if field.value():
            edit_url = reverse('admin:%s_%s_changelist' % info, current_app=field.field.widget.admin_site.name)
        widget.attrs['class'] = 'form-control'
        widget.attrs['id'] = 'id_{}'.format(field.name)
        if field.field.required and not self.is_inlines:
            widget.attrs['required'] = ''
        output = get_template('admin/widgets/model_select_widget.html')
        html_output = output.render(Context({
            'model_select_widget': widget.render(field.html_name, field.value(), attrs={
                'id': field.auto_id,
                'name': field.html_name,
            }),
            'value': field.value(),
            'id': field.auto_id,
            'add_url': add_url,
            'edit_url': edit_url,
            'add_name': 'add_id_{}'.format(field.html_name),
            'edit_name': 'edit_id_{}'.format(field.html_name)
        }))
        return html_output

    def render_model_multiple_choice_widgets(self, field):
        widget = field.field.widget.widget
        field.help_text = ''
        can_add_related = field.field.widget.can_add_related
        related_url = None
        if can_add_related:
            rel_to = field.field.widget.rel.to
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = reverse('admin:%s_%s_add' % info, current_app=field.field.widget.admin_site.name)
        widget.attrs['id'] = 'id_{}'.format(field.name)
        if field.field.required and not self.is_inlines:
            widget.attrs['required'] = ''
        output = get_template('admin/widgets/model_select_widget.html')
        rendered_output = widget.render(field.name, field.value(), attrs={'class': 'form-control'})
        rendered_output = rendered_output.replace('SelectFilter.init(', 'ActivateChosen(')
        rendered_output = rendered_output.replace('selectfilter', 'selectfilter form-control')
        html_output = output.render(Context({
            'model_select_widget': mark_safe(rendered_output),
            'related_url': related_url,
            'name': 'add_id_{}'.format(field.html_name)
        }))
        return html_output

    def render_readonly_widgets(self, field):
        widget = field.field.widget
        widget.attrs['id'] = 'id_{}'.format(field.name)
        rendered_output = widget.render(field.name, field.value(), attrs={
            'id': 'id_{}'.format(field.html_name),
            'class': 'form-control-static',
        })
        return rendered_output


@register.tag()
def custom_widget(parser, token):
    contents = token.split_contents()
    extra_attributes = {}
    if len(contents) > 2:
        for a in contents[2:]:
            kv = a.split('=')
            key = kv[0]
            value = kv[1]
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            extra_attributes[key] = value
    field_name = contents[1]
    extra_attributes['class'] = 'form-control'
    return BootstrapWidgetNode(field_name, extra_attributes)


@register.assignment_tag(takes_context=True)
def get_model(context, app_label, model_name):
    request = context['request']
    for model, model_admin in admin.site._registry.items():
        if app_label == model._meta.app_label and model_name == model._meta.model_name:
            has_module_perms = request.user.has_module_perms(app_label)

            if has_module_perms:
                perms = model_admin.get_model_perms(request)

                if True in perms.values():
                    info = (app_label, model._meta.model_name)
                    model_dict = {
                        'name': capfirst(model._meta.verbose_name_plural),
                        'object_name': model._meta.object_name,
                        'perms': perms,
                    }
                    if perms.get('change', False):
                        try:
                            model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=admin.site.name)
                        except NoReverseMatch:
                            pass
                    if perms.get('add', False):
                        try:
                            model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=admin.site.name)
                        except NoReverseMatch:
                            pass
                    return model_dict
            return None


@register.assignment_tag(takes_context=True)
def get_app_list(context):
    app_dict = {}
    request = context['request']
    for model, model_admin in admin.site._registry.items():
        app_label = model._meta.app_label
        has_module_perms = request.user.has_module_perms(app_label)

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                info = (app_label, model._meta.model_name)
                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                }
                if perms.get('change', False):
                    try:
                        model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=admin.site.name)
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=admin.site.name)
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    app_dict[app_label] = {
                        'name': apps.get_app_config(app_label).verbose_name,
                        'app_label': app_label,
                        'app_url': reverse(
                            'admin:app_list',
                            kwargs={'app_label': app_label},
                            current_app=admin.site.name,
                        ),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                    }

    # Sort the apps alphabetically.
    app_list = list(six.itervalues(app_dict))
    app_list.sort(key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])

    return app_list


@register.filter
def to_app_model_name(obj):
    return obj._meta.app_label + '_' + obj._meta.model_name
