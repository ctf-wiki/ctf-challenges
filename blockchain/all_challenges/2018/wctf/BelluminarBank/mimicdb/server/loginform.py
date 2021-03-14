from hashlib import md5

from wtforms import form, fields, validators
from user import User


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    username = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid user')

        if user.password != md5(self.password.data).hexdigest():
            raise validators.ValidationError('Invalid password')

    def get_user(self):
        return User.get(self.username.data)