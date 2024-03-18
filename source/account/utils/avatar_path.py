# import sys
# from pathlib import Path
#
# add path to modules from parent directory
# dir = str(Path(__file__).parent.parent)
# sys.path.append(dir)

# from ..models import UserAvatarModel


def avatar_path(instance, filename):
    return '{}_avatar_{}'.format(instance.user.id, filename)
