from django.db.models import TextChoices
from django.utils.translation import ugettext_lazy as _


class CurrencyChoices(TextChoices):
    USD = '$', _('USD')
    EUR = '€', _('EUR')
