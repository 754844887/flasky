from os import name
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(FlaskForm):
    name = StringField('name', [Length(min=4, max=64, message='用户名长度为4到64个字符！')])
    email = StringField('email', [Email(message='请输入正确的邮箱地址！')])
    password = PasswordField('password', [
        DataRequired(),
        EqualTo('password2', message='两次输入的密码不一致！')
    ])
    password2 = PasswordField('repeat password')