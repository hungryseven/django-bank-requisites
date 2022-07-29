from rest_framework import serializers
from django_bank_requisites.mixins import BankDetailsValidationMixin

from .models import OrganizationValidated, OrganizationUnvalidated

class UnvalidatedModelSerializer(BankDetailsValidationMixin, serializers.ModelSerializer):
    """
    Create serializer like this if you use BankDetailsUnvalidated abstract model.
    """

    # It's important to inherit BankDetailsValidationMixin Meta class
    # to have field-level validation
    class Meta(BankDetailsValidationMixin.Meta):
        model = OrganizationUnvalidated
        fields = "__all__"

class ValidatedModelSerializer(serializers.ModelSerializer):
    """
    If you use BankDetailsValidated abstract model serializer class looks as usual.
    """

    class Meta:
        model = OrganizationValidated
        fields = "__all__"