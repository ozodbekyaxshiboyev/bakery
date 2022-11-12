from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_amount(value):
    if value <= 0:
        raise ValidationError(
            _('Kiritilayotgan mablag` 0 dan katta bo`lishi kerak!'),
            params={'value': value},
        )
    return value