import re
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator, \
                            MinLengthValidator, EmailValidator


# find any decimal digit and characters oder than alphabetic
name_validators = [
    RegexValidator('[^a-zA-z_]', inverse_match=True),
    MaxLengthValidator(150, 'Name is too long (max 150).')
]

username_validators = [
    MinLengthValidator(4, 'Too short username (min 4).'),
    MaxLengthValidator(150, 'Too long username (max 150).')
]

email_validators = [
    MaxLengthValidator(150, 'Too long email (max 150).'),
    EmailValidator
]

# Password validator regex function
# check if is required characters:
# - digit
# - uppercase letter
# - character oder than alphanumeric
def password_regex_validator(password):
    regex = [
        re.compile('[A-Z]'),
        re.compile('\d'),
        re.compile('\W')
    ]

    for r in regex:
        if r.match(password) is not None:
            raise ValidationError(_('Invalid password. Must have digit, '
                                'one uppercase letter and special character.'),
                                code='invalid password')

password_validators = [
    MinLengthValidator(8, 'Too short password (min 8).'),
    MaxLengthValidator(150, 'Too long password (max 150).'),
    password_regex_validator
]
