from wtforms import TextField, PasswordField, validators
from forms.ipsecureform import IPSecureForm

def validate_login_password(form, field):
    login = form['login'].data
    password = form['password'].data

    from flask import current_app

    if login != current_app.config['USERNAME'] or password != current_app.config['PASSWORD']:
        raise validators.ValidationError('Wrong username or password')


class LoginForm(IPSecureForm):
    login = TextField('Login', [
        validators.Required(),
        ])

    password = PasswordField('New Password', [
        validators.Required(message='Password field is required'),
        validate_login_password
    ])

