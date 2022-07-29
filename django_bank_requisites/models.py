from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .base_validators import (is_bik_valid,
                              is_bank_account_code_check_num_valid,
                              is_ks_3_last_digits_valid,
                              is_code_length_valid,
                              is_code_structure_valid)
from .django_validators import *


class BankDetailsUnvalidated(models.Model):
    """
    Abstract model without bank details validation.
    """

    legal_address = models.CharField(verbose_name=_("Legal address"), max_length=255)
    inn = models.CharField(verbose_name=_("INN"), unique=True, max_length=12)
    kpp = models.CharField(verbose_name=_("KPP"), max_length=9)
    rs = models.CharField(verbose_name=_("RS"), unique=True, max_length=20)
    ks = models.CharField(verbose_name=_("KS"), blank=True, max_length=20)
    bik = models.CharField(verbose_name=_("BIK"), max_length=9)
    bank_name = models.CharField(verbose_name=_("Bank name"), max_length=255)

    class Meta:
        abstract = True

class BankDetailsValidated(models.Model):
    """
    Abstract model with bank details validation.
    """

    legal_address = models.CharField(verbose_name=_("Legal address"), max_length=255)
    inn = models.CharField(verbose_name=_("INN"), unique=True, max_length=12, validators=[validate_inn])
    kpp = models.CharField(verbose_name=_("KPP"), max_length=9, validators=[validate_kpp])
    rs = models.CharField(verbose_name=_("RS"), unique=True, max_length=20, validators=[validate_rs])
    ks = models.CharField(verbose_name=_("KS"), blank=True, max_length=20, validators=[validate_ks])
    bik = models.CharField(verbose_name=_("BIK"), max_length=9, validators=[validate_bik])
    bank_name = models.CharField(verbose_name=_("Bank name"), max_length=255)

    class Meta:
        abstract = True

    def clean(self):
        # Since RS and KS depends on BIK, validate it one more time
        if not is_bik_valid(bik=self.bik):
            return
        errors_dict = {}

        # Validate RS check num if code length and structure are valid
        rs_bik_digits = self.bik[-3:]
        if (is_code_length_valid(code=self.rs, length=(20,)) and
            is_code_structure_valid(code=self.rs) and
            not is_bank_account_code_check_num_valid(code=self.rs, bik_digits=rs_bik_digits)):
            errors_dict.update(rs=ValidationError(message=error_messages["check_num_bik"], code="invalid_check_num_or_bik"))

        if self.ks:
            # Firstly validate that the last 3 digits of KS are equal to the last 3 digits of BIK.
            # If it is true, validate KS check num if code length and structure are valid
            if not is_ks_3_last_digits_valid(ks=self.ks, bik=self.bik):
                errors_dict.update(ks=ValidationError(message=error_messages["ks_last_3"], code="invalid_ks"))
            else:
                ks_bik_digits = "0" + self.bik[4:6]
                if (is_code_length_valid(code=self.ks, length=(20,)) and
                    is_code_structure_valid(code=self.ks) and
                    not is_bank_account_code_check_num_valid(code=self.ks, bik_digits=ks_bik_digits)):
                    errors_dict.update(ks=ValidationError(message=error_messages["check_num_bik"], code="invalid_check_num_or_bik"))

        if errors_dict:
            raise ValidationError(errors_dict)