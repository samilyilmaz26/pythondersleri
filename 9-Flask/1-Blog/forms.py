from wtforms import Form, BooleanField, StringField, PasswordField, validators,TextAreaField

class RegistrationForm(Form):
    username = StringField('Kullanıcı İsmi', [validators.Length(min=4, max=25)])
    email = StringField('EPosta  Addres', [validators.Length(min=6, max=35)])
    password = PasswordField('Şifre ', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Şifreler Uyumlu olmalı')
    ])
    confirm = PasswordField('Şifre Tekrar ')
    accept_tos = BooleanField('Şartları Okudum Kabul Ediyorum ', [validators.DataRequired()])
class LoginForm(Form):
    username = StringField('Kullanıcı İsmi' )
    password = PasswordField('Şifre ' )
class ArticleForm(Form):
    title = StringField('Başlık', [validators.Length(min=4,max=50)])
    content = TextAreaField("İçerik" ,[validators.Length(min=10,max=1000)])