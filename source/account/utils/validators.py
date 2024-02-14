import re
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxLengthValidator, \
                            MinLengthValidator, EmailValidator


# find any decimal digit and characters oder than alphabetic
NameValidator = RegexValidator('[^a-zA-z_]', inverse_match=True)

MaxNameLengthValidator = MaxLengthValidator(150, 'Name is too long (max 150).')

username_validators = [
                        MinLengthValidator(4, 'Too short username (min 4).'),
                        MaxLengthValidator(150, 'Too long username (max 150).')
                    ]

email_validators = [ 
                    MaxLengthValidator(150, 'Too long email (max 150).'),
                    EmailValidator
                ]

# check if is required characters:
# - digit
# - uppercase letter
# - character oder than alphanumeric
def password_validator(password):
    regex = [
        re.compile('[A-Z]'),
        re.compile('\d'),
        re.compile('\W')
    ]

    for r in regex:
        if r.match(password) is None:
            raise ValidationError(_('Invalid password. Must have digit, '
                                'one uppercase letter and special character.'),
                                code='invalid password')
