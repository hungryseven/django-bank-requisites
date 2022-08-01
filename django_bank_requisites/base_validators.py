INN_COEFFICIENTS = {
    "inn_10": (2, 4, 10, 3, 5, 9, 4, 6, 8),
    "inn_12_penult": (7, 2, 4, 10, 3, 5, 9, 4, 6, 8),
    "inn_12_last": (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
}
BANK_ACCOUNT_COEFFICIENTS = (7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1)
FIRST_3_KS_DIGITS = "301"

### HELPER FUNCS ###

def _calculate_digits_sum(code: str, coefs: tuple) -> int:
    """
    Calculates the sum of the products of the code digit by the corresponding coefficient.
    """
    sum = 0
    for digit, coef in zip(code, coefs):
        sum += int(digit) * coef
    return sum

def _compare_inn_check_nums(code: str, num_to_check: int, divider: int, coefs: tuple) -> bool:
    """
    Compares INN calculated check number and code check number.
    """
    sum = _calculate_digits_sum(code=code, coefs=coefs)
    mod = sum % divider
    if mod < 10 and mod == num_to_check or mod >= 10 and mod % 10 == num_to_check:
        return True
    return False

def _compare_ogrn_check_nums(code: str, num_to_check: int, divider: int) -> bool:
    """
    Compares OGRN calculated check number and code check number.
    """
    mod = int(code) % divider
    if mod < 10 and mod == num_to_check or mod >= 10 and int(str(mod)[-1]) == num_to_check:
        return True
    return False
    
### BASE HELPER VALIDATORS ###

def is_code_length_valid(code: str, length: tuple) -> bool:
    """
    Validates code length.
    The code may have a different length depending on whether
    it is a legal entity or an individual entrepreneur.
    """
    if not all(list(map(lambda x: isinstance(x, int), length))):
        raise TypeError("All length values must be of type int")
    return (True
            if len(code) in length
            else False)

def is_code_structure_valid(code: str) -> bool:
    """
    Validates if the code consists only of digits.
    """
    return (True
            if all(list(map(lambda x: x.isdigit(), code)))
            else False)

def is_inn_check_num_valid(inn: str) -> bool:
    """
    Validates INN check numbers depending on code length.
    """
    last_digit = int(inn[-1])
    if len(inn) == 10:
        return _compare_inn_check_nums(inn, last_digit, 11, INN_COEFFICIENTS["inn_10"])
    elif len(inn) == 12:
        penult_digit = int(inn[-2])
        return (_compare_inn_check_nums(inn, penult_digit, 11, INN_COEFFICIENTS["inn_12_penult"]) and
                _compare_inn_check_nums(inn, last_digit, 11, INN_COEFFICIENTS["inn_12_last"]))

def is_ogrn_check_num_valid(ogrn: str) -> bool:
    """
    Validates OGRN check numbers depending on code length.
    """
    last_digit = int(ogrn[-1])
    if len(ogrn) == 13:
        return _compare_ogrn_check_nums(ogrn[:12], last_digit, 11)
    elif len(ogrn) == 15:
        return _compare_ogrn_check_nums(ogrn[:14], last_digit, 13)

def is_bank_account_code_check_num_valid(code: str, bik_digits: str) -> bool:
    """
    Validates RS (расчетный счет) or KS (корреспондентский счет)
    check number depending on BIK.

    Params:
            code (str): RS or KS code which will be checked
            bik_digits (str): Digits to be added to the beginning of the RS or KS code
                              (7, 8, 9 BIK digits for RS code
                              or 0 (zero) and 5, 6 BIK digits for KS code)
    """
    code_to_check = bik_digits + code
    sum = _calculate_digits_sum(code=code_to_check, coefs=BANK_ACCOUNT_COEFFICIENTS)
    return (True
            if int(str(sum)[-1]) == 0
            else False)

def is_ks_3_last_digits_valid(ks: str, bik: str) -> bool:
    """
    Validates that the last 3 digits of KS match to the last 3 digits of BIK
    """
    return (True
            if ks[-3:] == bik[-3:]
            else False)

def is_ks_3_first_digits_valid(ks: str) -> bool:
    """
    Validates that the first 3 digits of KS match sequence '301'
    """
    return (True
            if ks[:3] == FIRST_3_KS_DIGITS
            else False)

### BASE CODE VALIDATORS ###

def is_inn_valid(inn: str) -> bool:
    """
    Validates INN with all checks.
    """
    return (is_code_length_valid(code=inn, length=(10, 12)) and
            is_code_structure_valid(code=inn) and
            is_inn_check_num_valid(inn=inn))

def is_kpp_valid(kpp: str) -> bool:
    """
    Validates KPP with all checks.
    """
    return (is_code_length_valid(code=kpp, length=(9,)) and
            is_code_structure_valid(code=kpp))

def is_ogrn_valid(ogrn: str) -> bool:
    """
    Validates OGRN with all checks.
    """
    return (is_code_length_valid(code=ogrn, length=(13, 15)) and
            is_code_structure_valid(code=ogrn) and
            is_ogrn_check_num_valid(ogrn=ogrn))

def is_bik_valid(bik: str) -> bool:
    """
    Validates BIK with all checks.
    """
    return (is_code_length_valid(code=bik, length=(9,)) and
            is_code_structure_valid(code=bik))

def is_rs_valid(rs: str, bik: str) -> bool:
    """
    Validates RS (расчетный счет) with all checks.
    """
    if not is_bik_valid(bik=bik):
        return False
    bik_digits = bik[-3:]
    return (is_code_length_valid(code=rs, length=(20,)) and
            is_code_structure_valid(code=rs) and
            is_bank_account_code_check_num_valid(code=rs, bik_digits=bik_digits))

def is_ks_valid(ks: str, bik: str) -> bool:
    """
    Validates KS (корреспондентский счет) with all checks.
    """
    if not is_bik_valid(bik=bik):
        return False
    if not is_ks_3_last_digits_valid(ks=ks, bik=bik):
        return False
    if not is_ks_3_first_digits_valid(ks=ks):
        return False
    bik_digits = "0" + bik[4:6]
    return (is_code_length_valid(code=ks, length=(20,)) and
            is_code_structure_valid(code=ks) and
            is_bank_account_code_check_num_valid(code=ks, bik_digits=bik_digits))
