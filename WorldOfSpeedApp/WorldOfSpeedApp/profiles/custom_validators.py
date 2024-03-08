from django.core.exceptions import ValidationError


def user_name_validator(username):
    for char in username:
        if not (char.isalnum() or char == '_'):
            raise ValidationError("Username must contain only letters, digits, and underscores!")


def custom_minlength_validator(username):
    if len(username) < 3:
        raise ValidationError("Username must be at least 3 chars long!")


def validate_picture_format(value):
    allowed_picture_formats = ['jpg', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'gif']
    url_parts = value.split('.')
    url_ext = url_parts[-1].lower()

    if url_ext not in allowed_picture_formats:
        raise ValidationError(
            'Invalid picture format. Only JPG, JPEG, PNG, BMP, TIF, TIFF, and GIF formats are allowed.'
        )
