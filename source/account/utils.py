from io import StringIO

from django.db import models
from django.contrib.auth.models import User

from .models import UserAvatarModel


def get_avatar_name(user):
    if not isinstance(user, User):
        raise TypeError('user is not User object.')

    try:
        avatar = UserAvatarModel.objects.get(user=user).avatar

        if avatar.size:
            return avatar.name
        else:
            return None
    except models.ObjectDoesNotExist:
        return None
    except FileNotFoundError:
        return None


def gen_html_validation_errors(invalid_fields, tab=0):
    if not isinstance(invalid_fields, dict):
        raise TypeError('invalid_fields is not dict.')
        return None

    if tab:
        tab = tab * '\t'
    else:
        tab = ''

    gen_html = StringIO()
    gen_html.write(f'{tab}<div class="overflow-auto errors-textbox">\n'
                   f'{tab}\t<table>\n')

    for field in invalid_fields.keys():
        if field == 'password2':
            continue

        gen_html.write(f'{tab}\t\t<tr>\n'
                       f'{2*tab}<th class="invalid-field">'
                       f'<span>{field}: </span></th>\n'
                       f'{2*tab}<th>\n')

        for error_content in invalid_fields[field]:
            error_message = error_content['message']
            gen_html.write(f'{2*tab}\t<span>{error_message}</span><br>\n')

        gen_html.write(f'{2*tab}</th>\n')

    gen_html.write(f'{tab}\t</table>\n'
                   f'{tab}</div>')

    return gen_html.getvalue()
