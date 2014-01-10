from wtforms import TextField, PasswordField, validators, TextAreaField
from forms.ipsecureform import IPSecureForm


class EditForm(IPSecureForm):
    name = TextField('Name', [
        validators.Required(),
        ])

    ios = TextField('iOS link', [
        validators.Required(),
        ])

    android = TextField('Android link', [
    validators.Required(),
    ])

    texts = TextAreaField('Texts', [
        validators.Required(),
        ])
