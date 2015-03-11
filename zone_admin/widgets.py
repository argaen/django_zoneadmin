from django import forms
from django.forms.widgets import flatatt
from django.utils.html import escape


class TinyMCEWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        final_attrs['name'] = name
        final_attrs['class'] = 'form-control tinymce'

        html = ['<textarea%s>%s</textarea>' % (flatatt(final_attrs), escape(value))]
        return '\n'.join(html)
