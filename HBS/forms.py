from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DateTimeField, SelectField, BooleanField
from wtforms.validators import DataRequired




class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password= PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Giriş Yap')


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password= PasswordField('password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Üye Ol ')


class MaximForm(FlaskForm):
    maxim = TextAreaField(validators=[DataRequired()])
    select = SelectField(choices=[
        ('1', 'Ayet'),
        ('2', 'Hadis'),
        ('3', 'Söz'),

    ])
    author = StringField()
    show = BooleanField()
    submit = SubmitField('Ekle')


class SettingsForm(FlaskForm):
    maxim_number = IntegerField()
    # maxim_date = DateTimeField(format="%H:%M")
    submit = SubmitField('Duzenle')