from wtforms import TextField, PasswordField, validators, TextAreaField, BooleanField
from forms.ipsecureform import IPSecureForm
from flask import flash

def validate_texts_content(form, field):
    texts = form['texts'].data

    raw_announces = texts.strip()
    announces = {}
    lines = raw_announces.split("\n")

    for line in lines:
        items = line.split("|")
        if len(items) > 1:
            announces[items[0]] = items[1]

    if len(announces) == 0:
        flash('Announces field is empty. This field have to have one o more lines with format: lang|description')
        raise validators.ValidationError('Announces field is empty. This field have to have one o more lines with format: lang|description')

    if not 'default' in announces:
        flash('Announce field have to contain "default" item: default|Some description ')
        raise validators.ValidationError('Announce field have to contain "default" item: default|Some description ')

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
        validate_texts_content,
        ],
        description='This field have to have one o more lines with format: lang|description. '
                    'Field have to have one element with key "default".\n'
                    'Example:\n'
                    'default|Some announce in eanglish\n'
                    'ru_RU|some announce in russian')

    delete = BooleanField('Delete item')

