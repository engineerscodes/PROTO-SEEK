
from django.core.exceptions import ValidationError


def file_size(values):

    if values.size >4e+8 :
        raise ValidationError("MAX FILE SHOULD BE 50MB")