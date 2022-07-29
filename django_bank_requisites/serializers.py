from rest_framework import serializers

from .mixins import BankDetailsValidationMixin
from .django_validators import (validate_inn,
                                validate_kpp,
                                validate_rs,
                                validate_ks,
                                validate_bik)


class BankDetailsSerializer(BankDetailsValidationMixin, serializers.Serializer):
    """
    Base bank details serializer which doesn't need model with all validation steps.
    """

    legal_address = serializers.CharField(max_length=255)
    inn = serializers.CharField(validators=[validate_inn])
    kpp = serializers.CharField(validators=[validate_kpp])
    rs = serializers.CharField(validators=[validate_rs])
    ks = serializers.CharField(validators=[validate_ks])
    bik = serializers.CharField(validators=[validate_bik])
    bank_name = serializers.CharField(max_length=255)