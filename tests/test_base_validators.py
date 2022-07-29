from django_bank_requisites.base_validators import *
from django_bank_requisites.base_validators import (_calculate_digits_sum,
                                               _compare_inn_check_nums,
                                               _compare_ogrn_check_nums)

### HELPER FUNCS TESTS ###

def test_calculate_digits_sum_func():
    sum = _calculate_digits_sum(code="7830002293", coefs=INN_COEFFICIENTS["inn_10"])
    assert sum == 168
    sum = _calculate_digits_sum(code="500100732259", coefs=INN_COEFFICIENTS["inn_12_penult"])
    assert sum == 148
    sum = _calculate_digits_sum(code="500100732259", coefs=INN_COEFFICIENTS["inn_12_last"])
    assert sum == 141

def test_compare_inn_check_nums_func():
    result = _compare_inn_check_nums(code="7830002293", num_to_check=3, divider=11, coefs=INN_COEFFICIENTS["inn_10"])
    assert result == True
    result = _compare_inn_check_nums(code="500100732259", num_to_check=5, divider=11, coefs=INN_COEFFICIENTS["inn_12_penult"])
    assert result == True
    result = _compare_inn_check_nums(code="500100732259", num_to_check=9, divider=11, coefs=INN_COEFFICIENTS["inn_12_last"])
    assert result == True

    result = _compare_inn_check_nums(code="7702038150", num_to_check=1, divider=11, coefs=INN_COEFFICIENTS["inn_10"])
    assert result == False
    result = _compare_inn_check_nums(code="740102294724", num_to_check=3, divider=11, coefs=INN_COEFFICIENTS["inn_12_penult"])
    assert result == False
    result = _compare_inn_check_nums(code="740102294724", num_to_check=5, divider=11, coefs=INN_COEFFICIENTS["inn_12_last"])
    assert result == False

def test_compare_ogrn_check_nums_func():
    result = _compare_ogrn_check_nums(code="103500611008", num_to_check=3, divider=11)
    assert result == True
    result = _compare_ogrn_check_nums(code="30450011600015", num_to_check=7, divider=13)
    assert result == True
    result = _compare_ogrn_check_nums(code="30446321070021", num_to_check=2, divider=13)
    assert result == True

    result = _compare_ogrn_check_nums(code="102770009628", num_to_check=1, divider=11)
    assert result == False
    result = _compare_ogrn_check_nums(code="30674521880001", num_to_check=3, divider=13)
    assert result == False

### BASE HELPER VALIDATORS TESTS ###

def test_is_code_length_valid_func():
    # Valid length
    result = is_code_length_valid(code="1234567890", length=(10,))
    assert result == True

    # Invalid length
    result = is_code_length_valid(code="1234567890", length=(9,))
    assert result == False

def test_is_code_structure_valid_func():
    # Valid code
    result = is_code_structure_valid(code="1234567890")
    assert result == True

    # Invalid code
    result = is_code_structure_valid(code="1234567890q")
    assert result == False

def test_is_inn_check_num_valid_func():
    # Valid INNs (existing codes)
    result = is_inn_check_num_valid("7702038150")
    assert result == True
    result = is_inn_check_num_valid("7705002602")
    assert result == True
    result = is_inn_check_num_valid("500100732259")
    assert result == True
    result = is_inn_check_num_valid("740102294724")
    assert result == True

    # Invalid INNs
    result = is_inn_check_num_valid("1234567890")
    assert result == False
    result = is_inn_check_num_valid("1122334455")
    assert result == False
    result = is_inn_check_num_valid("123456789012")
    assert result == False
    result = is_inn_check_num_valid("112233445566")
    assert result == False

def test_is_ogrn_check_num_valid_func():
    # Valid OGRNs (existing codes)
    result = is_ogrn_check_num_valid("1035006110083")
    assert result == True
    result = is_ogrn_check_num_valid("1037739010891")
    assert result == True
    result = is_ogrn_check_num_valid("304500116000157")
    assert result == True
    result = is_ogrn_check_num_valid("304463210700212")
    assert result == True

    # Invalid OGRNs
    result = is_ogrn_check_num_valid("1231231231234")
    assert result == False
    result = is_ogrn_check_num_valid("1122334455667")
    assert result == False
    result = is_ogrn_check_num_valid("123123123123123")
    assert result == False
    result = is_ogrn_check_num_valid("112233445566778")
    assert result == False

def test_is_bank_account_code_check_num_valid_func():
    # Valid RS and BIK
    result = is_bank_account_code_check_num_valid(code="40602810900070000045", bik_digits="411")
    assert result == True
    # Valid KS and BIK
    result = is_bank_account_code_check_num_valid(code="30101810145250000411", bik_digits="025")
    assert result == True

    # Invalid RS and BIK
    result = is_bank_account_code_check_num_valid(code="12312312312312312312", bik_digits="973")
    assert result == False
    # Valid KS and BIK
    result = is_bank_account_code_check_num_valid(code="78978978978978978978", bik_digits="083")
    assert result == False

def test_is_ks_3_last_digits_valid_func():
    # Digits are match
    result = is_ks_3_last_digits_valid(ks="30101810145250000411", bik="044525411")
    assert result == True

    # Digits are not match
    result = is_ks_3_last_digits_valid(ks="30101810145250000412", bik="044525411")
    assert result == False

def test_is_ks_3_first_digits_valid_func():
    # Digits are match
    result = is_ks_3_first_digits_valid(ks="30101810145250000411")
    assert result == True

    # Digits are not match
    result = is_ks_3_first_digits_valid(ks="30001810145250000412")
    assert result == False

### BASE VALIDATORS TESTS ###

def test_is_inn_valid_func():
    # Valid INNs (existing codes)
    result = is_inn_valid("7451448020")
    assert result == True
    result = is_inn_valid("744819576984")
    assert result == True

    # Invalid INN length
    result = is_inn_valid("12345678912")
    assert result == False

    # Invalid INN structure
    result = is_inn_valid("12345q6789")
    assert result == False
    result = is_inn_valid("12345ww89012")
    assert result == False

    # Invalid INNs
    result = is_inn_valid("7830000978")
    assert result == False
    result = is_inn_valid("744703315311")
    assert result == False

def test_is_kpp_valid_func():
    # Valid KPP (existing code)
    result = is_kpp_valid("770201001")
    assert result == True

    # Invalid KPP length
    result = is_kpp_valid("12345678")
    assert result == False

    # Invalid KPP structure
    result = is_kpp_valid("q12345678")
    assert result == False

def test_is_ogrn_valid_func():
    # Valid OGRNs (existing codes)
    result = is_ogrn_valid("1027700096280")
    assert result == True
    result = is_ogrn_valid("306745218800012")
    assert result == True

    # Invalid OGRN length
    result = is_ogrn_valid("12345678912345")
    assert result == False

    # Invalid OGRN structure
    result = is_ogrn_valid("10277qwe96280")
    assert result == False
    result = is_ogrn_valid("30674521q800012")
    assert result == False

    # Invalid OGRNs
    result = is_ogrn_valid("1928374650777")
    assert result == False
    result = is_ogrn_valid("918273645000559")
    assert result == False

def test_is_bik_valid_func():
    # Valid BIK (existing code)
    result = is_bik_valid("047501602")
    assert result == True

    # Invalid BIK length
    result = is_bik_valid("12345678")
    assert result == False

    # Invalid BIK structure
    result = is_bik_valid("q12345678")
    assert result == False

def test_is_rs_valid_func():
    # Valid RS and BIK
    result = is_rs_valid(rs="40602810900070000045", bik="044525411")
    assert result == True
    result = is_rs_valid(rs="40702810500000000014", bik="044544512")
    assert result == True

    # Invalid BIK
    result = is_rs_valid(rs="40602810900070000045", bik="04455411")
    assert result == False
    result = is_rs_valid(rs="40602810900070000045", bik="0445q5411")
    assert result == False

    # Invalid RS
    result = is_rs_valid(rs="4070281050000000014", bik="044544512")
    assert result == False
    result = is_rs_valid(rs="407028105000000q014", bik="044544512")
    assert result == False

def test_is_ks_valid_func():
    # Valid KS and BIK
    result = is_ks_valid(ks="30101810145250000411", bik="044525411")
    assert result == True
    result = is_ks_valid(ks="30101810000000000608", bik="042406608")
    assert result == True

    # Invalid BIK
    result = is_ks_valid(ks="30101810145250000411", bik="04455411")
    assert result == False
    result = is_ks_valid(ks="30101810145250000411", bik="0445q5411")
    assert result == False

    # Last 3 digits of the codes are not equal
    result = is_ks_valid(ks="30101810145250000412", bik="044525411")
    assert result == False

    # Invalid KS
    result = is_ks_valid(ks="3010000000000000097", bik="045525977")
    assert result == False
    result = is_ks_valid(ks="3010000000000000q977", bik="045525977")
    assert result == False