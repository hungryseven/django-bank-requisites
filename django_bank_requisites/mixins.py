from rest_framework import serializers

from .base_validators import is_bank_account_code_check_num_valid, is_ks_3_last_digits_valid
from .django_validators import *

class SaveMethodMixin:
    """
    If you want clean() method from BankDetailsValidated model works in DRF
    simply inherit your model from SaveMethodMixin:
    
    class MyModel(SaveMethodMixin, BankDetailsValidated):

        pass

    If you need to implement custom save method for your model,
    just add self.clean() line in it.
    
    Then add this line in your DRF settings:
    REST_FRAMEWORK = {
        .....
        'EXCEPTION_HANDLER': 'bank_details.exception_handler.exception_handler',
        .....
    }
    """

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class BankDetailsValidationMixin:
    """
    Mixin includes different levels of serializer validation.
    1) Field level validation
    2) Validation that requires access to multiple fields

    If you are using a model without validation simply inherit your serializer
    and Meta in it from this mixin:

    class MySerializer(BankDetailsValidationMixin, serializers.ModelSerializer):

        class Meta(BankDetailsValidationMixin.Meta):

            model = <your model>
            fields/exclude = <fields to include/exclude>

    If you are using a model with validation and don't want to handle
    Django ValidationError and convert it into DRF ValidationError
    simply inherit your serializer from this mixin:

    class MySerializer(BankDetailsValidationMixin, serializers.ModelSerializer):

        pass
    """

    class Meta:
        extra_kwargs = {
            "inn": {
                "validators": [validate_inn]
            },
            "kpp": {
                "validators": [validate_kpp]
            },
            "rs": {
                "validators": [validate_rs]
            },
            "ks": {
                "validators": [validate_ks]
            },
            "bik": {
                "validators": [validate_bik]
            }
        }
    
    def validate(self, data):
        # In serializers we don't need the extra validators,
        # that were at the field level, again like in models.
        # This method will work if all field level validators are pass.
        errors_dict = {}

        # Validate RS check num
        rs_bik_digits = data["bik"][-3:]
        if not is_bank_account_code_check_num_valid(code=data["rs"], bik_digits=rs_bik_digits):
            errors_dict.update(rs=error_messages["check_num_bik"])

        # Firstly validate that the last 3 digits of KS are equal to the last 3 digits of BIK.
        # If it is true, validate KS check num
        if data["ks"]:
            if not is_ks_3_last_digits_valid(ks=data["ks"], bik=data["bik"]):
                errors_dict.update(ks=error_messages["ks_last_3"])
            else:
                ks_bik_digits = "0" + data["bik"][4:6]
                if not is_bank_account_code_check_num_valid(code=data["ks"], bik_digits=ks_bik_digits):
                    errors_dict.update(ks=error_messages["check_num_bik"])

        if errors_dict:
            raise serializers.ValidationError(errors_dict)
            
        return data