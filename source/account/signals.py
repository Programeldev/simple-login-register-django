from pathlib import Path


def delete_avatar(sender, instance, **kwargs):
    Path(instance.avatar.path).unlink(missing_ok=True)
