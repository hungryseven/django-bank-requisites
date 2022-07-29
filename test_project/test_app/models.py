from django.db import models
from django_bank_requisites.models import BankDetailsValidated, BankDetailsUnvalidated
from django_bank_requisites.mixins import SaveMethodMixin

class OrganizationValidated(SaveMethodMixin, BankDetailsValidated):
    """
    This model has all validation on it's own level.
    """

    organization_name = models.CharField(verbose_name='Organization name', max_length=255)

class OrganizationUnvalidated(BankDetailsUnvalidated):
    """
    If you use unvalidated model don't forget to add BankDetailsValidationMixin to your serializer.
    """

    organization_name = models.CharField(verbose_name='Organization name', max_length=255)