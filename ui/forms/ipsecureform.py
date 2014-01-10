from wtforms.ext.csrf import SecureForm
from hashlib import md5

from flask import current_app


class IPSecureForm(SecureForm):
    """
    Generate a CSRF token based on the user's IP.

    TODO: this form copied from tutorial, it has a comment: "I am probably not very
    secure, so don't use me."
    """

    def generate_csrf_token(self, csrf_context):
        # csrf_context is passed transparently from the form constructor,
        # in this case it's the IP address of the user
        token = md5(current_app.config['SECRET_KEY'] + csrf_context).hexdigest()
        return token

    def validate_csrf_token(self, field):
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')
