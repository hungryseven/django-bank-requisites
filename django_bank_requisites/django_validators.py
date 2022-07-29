from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .base_validators import *

error_messages = {
    "length": _("Invalid code length."),
    "structure": _("Code must contain only digits."),
    "check_num": _("Checknum calculated incorrectly. Enter correct code."),
    "check_num_bik": _("Checknum calculated incorrectly. Enter correct code or check BIK."),
    "ks_last_3": _("Last 3 digits of the KS must match last 3 digits of the BIK."),
    "ks_first_3": _("First 3 digits of the KS must match sequence '301'."),
}

def validate_length_and_structure(value, length: tuple):
    """
    Validates code length and structure.
    """
    errors = []
    if not is_code_length_valid(code=value, length=length):
        errors.append(ValidationError(message=error_messages["length"], code="invalid_length"))
    if not is_code_structure_valid(code=value):
        errors.append(ValidationError(message=error_messages["structure"], code="invalid_structure"))
    if errors:
        raise ValidationError(errors)
    
def validate_inn(value):
    """
    Validates INN length, structure and check nums.
    """
    validate_length_and_structure(value=value, length=(10, 12))
    if not is_inn_check_num_valid(inn=value):
        raise ValidationError(message=error_messages["check_num"], code="invalid_check_num")

def validate_kpp(value):
    """
    Validates KPP length and structure.
    """
    validate_length_and_structure(value=value, length=(9,))

def validate_ogrn(value):
    """
    Validates INN length, structure and check nums.
    """
    validate_length_and_structure(value=value, length=(13, 15))
    if not is_ogrn_check_num_valid(ogrn=value):
        raise ValidationError(message=error_messages["check_num"], code="invalid_check_num")

def validate_bik(value):
    """
    Validates BIK length and structure.
    """
    validate_length_and_structure(value=value, length=(9,))

def validate_rs(value):
    """
    Validates RS (расчетный счет) length and structure.
    """
    validate_length_and_structure(value=value, length=(20,))

def validate_ks(value):
    """
    Validates KS (корреспондентский счет) length and structure.
    """
    validate_length_and_structure(value=value, length=(20,))
    if not is_ks_3_first_digits_valid(ks=value):
        raise ValidationError(message=error_messages["ks_first_3"], code="invalid_ks")