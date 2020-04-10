from wtforms import widgets

try:
    from html import escape
except ImportError:
    from cgi import escape

from wtforms.compat import text_type


class Input(widgets.core.Input):
    def __call__(self, field, **kwargs):
        classes = ['form-control']
        if field.errors:
            classes.append('is-invalid')
        kwargs['class'] = kwargs['class_'] = ' '.join(classes)
        return super(Input, self).__call__(field, **kwargs)


class TextInput(Input):
    input_type = 'text'


class PasswordInput(Input):
    input_type = 'password'


class TextArea(object):
    """
    Renders a multi-line text area.

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        classes = ['form-control']

        # fixme in-invalid class invalid
        if field.errors:
            classes.append('is-invalid')
        kwargs['class'] = kwargs['class_'] = ' '.join(classes)
        return widgets.core.HTMLString('<textarea %s>%s</textarea>' % (
            widgets.core.html_params(name=field.name, **kwargs),
            escape(text_type(field._value()), quote=False)
        ))
