import re
from wtforms.form import Form
from wtforms.fields import StringField
from wtforms.validators import ValidationError
from wtforms import validators
from .core import TextInput, PasswordInput, TextArea

regex_email = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


class RegistrationForm(Form):
    username = StringField(u"用户名",
                           [validators.data_required(), validators.length(min=3, max=100)],
                           widget=TextInput()
                           )

    email = StringField(u"邮箱",
                        [validators.data_required(), validators.length(min=3, max=100)],
                        widget=TextInput()
                        )

    password = StringField(u"密码",
                           [validators.data_required(), validators.length(min=3, max=100)],
                           widget=TextInput()
                           )

    def validate_email(self, field):
        if not re.search(regex_email, field.data):
            raise ValidationError(u'Must be an email')


class LoginForm(Form):
    username = StringField(u"用户名",
                           [validators.data_required(), validators.length(min=3, max=100)],
                           widget=TextInput()
                           )

    password = StringField(u"密码",
                           [validators.data_required(), validators.length(min=3, max=100)],
                           widget=PasswordInput()
                           )


class TopicForm(Form):
    title = StringField(u"标题",
                        [validators.data_required(), validators.length(min=3, max=255)],
                        widget=TextInput()
                        )

    content = StringField(u"内容",
                          [validators.data_required(), validators.length(min=3, max=5000)],
                          widget=TextArea(),
                          render_kw={'rows': 10}
                          )


class ReplyForm(Form):
    content = StringField(u"内容",
                          [validators.data_required(), validators.length(min=3, max=5000)],
                          widget=TextArea()
                          )
