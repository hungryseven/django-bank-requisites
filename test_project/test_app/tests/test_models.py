from django.test import TestCase
from django.core.exceptions import ValidationError

from test_project.test_app.models import OrganizationValidated
from django_bank_requisites.django_validators import error_messages

class BankDetailsValidatedModelTestCase(TestCase):
    """
    Tests for abstract validated bank details model.
    """

    def setUp(self):
        self.model = OrganizationValidated
        self.data = {
            "organization_name": "ГУП ‟Московский метрополитен‟",
            "legal_address": "129110, город Москва, пр-кт Мира, д. 41 стр. 2",
            "inn": "7702038150",
            "kpp": "770201001",
            "rs": "40602810900070000003",
            "ks": "30101810500000000219",
            "bik": "044525219",
            "bank_name": "ОАО ‟Банк Москвы‟ г. Москва"
        }

    def test_model_with_valid_data(self):
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            pass
        else:
            org.save()
        orgs_count = OrganizationValidated.objects.count()
        self.assertEqual(orgs_count, 1)

    def test_model_legal_address_validation(self):
        # Blank legal_address
        self.data["legal_address"] = ""
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("legal_address", ""))
            self.assertIn("This field cannot be blank.", e.message_dict["legal_address"])

        # Invalid legal_address length
        self.data["legal_address"] = "0" * 256
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("legal_address", ""))

    def test_model_bank_name_validation(self):
        # Blank bank_name
        self.data["bank_name"] = ""
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("bank_name", ""))
            self.assertIn("This field cannot be blank.", e.message_dict["bank_name"])

        # Invalid bank_name length
        self.data["bank_name"] = "0" * 256
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("bank_name", ""))

    def test_model_inn_validation(self):
        # Blank INN
        self.data["inn"] = ""
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("inn", ""))
            self.assertIn("This field cannot be blank.", e.message_dict["inn"])

        # Invalid INN length
        self.data["inn"] = "77020381501"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("inn", ""))
            self.assertIn(error_messages["length"], e.message_dict["inn"])

        # Invalid INN structure
        self.data["inn"] = "770203815q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("inn", ""))
            self.assertIn(error_messages["structure"], e.message_dict["inn"])

        # Invalid INN length and structure
        self.data["inn"] = "7702038150q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("inn", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), e.message_dict["inn"])

        # Invalid INN 
        self.data["inn"] = "7702038151"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("inn", ""))
            self.assertIn(error_messages["check_num"], e.message_dict["inn"])

    def test_model_kpp_validation(self):
        # Blank KPP
        self.data["kpp"] = ""
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("kpp", ""))
            self.assertIn("This field cannot be blank.", e.message_dict["kpp"])

        # Invalid KPP length
        self.data["kpp"] = "7702010011"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("kpp", ""))
            self.assertIn(error_messages["length"], e.message_dict["kpp"])

        # Invalid KPP structure
        self.data["kpp"] = "77020100q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("kpp", ""))
            self.assertIn(error_messages["structure"], e.message_dict["kpp"])

        # Invalid KPP length and structure
        self.data["kpp"] = "770201001q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("kpp", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), e.message_dict["kpp"])

    def test_model_bik_validation(self):
        # Blank BIK
        self.data["bik"] = ""
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("bik", ""))
            self.assertIn("This field cannot be blank.", e.message_dict["bik"])

        # Invalid BIK length
        self.data["bik"] = "04452521"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("bik", ""))
            self.assertIn(error_messages["length"], e.message_dict["bik"])

        # Invalid BIK structure
        self.data["bik"] = "04452521q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("bik", ""))
            self.assertIn(error_messages["structure"], e.message_dict["bik"])

        # Invalid BIK length and structure
        self.data["bik"] = "044525219q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("bik", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), e.message_dict["bik"])

    def test_model_rs_validation(self):
        # Blank RS
        self.data["rs"] = ""
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("rs", ""))
            self.assertIn("This field cannot be blank.", e.message_dict["rs"])

        # Invalid RS length
        self.data["rs"] = "4060281090007000000"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("rs", ""))
            self.assertIn(error_messages["length"], e.message_dict["rs"])

        # Invalid RS structure
        self.data["rs"] = "4060281090007000000q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("rs", ""))
            self.assertIn(error_messages["structure"], e.message_dict["rs"])

        # Invalid RS length and structure
        self.data["rs"] = "40602810900070000003q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("rs", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), e.message_dict["rs"])

        # Invalid RS and valid BIK
        self.data["rs"] = "40602810900070000004"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("rs", ""))
            self.assertIn(error_messages["check_num_bik"], e.message_dict["rs"])

        # Valid RS and invalid BIK
        self.data["bik"] = "044525218"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("rs", ""))
            self.assertIn(error_messages["check_num_bik"], e.message_dict["rs"])

    def test_model_ks_validation(self):
        # Invalid KS length
        self.data["ks"] = "3010181050000000219"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn(error_messages["length"], e.message_dict["ks"])

        # Invalid KS structure
        self.data["ks"] = "3010181050000000q219"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn(error_messages["structure"], e.message_dict["ks"])

        # Invalid KS length and structure
        self.data["ks"] = "30101810500000000219q"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), e.message_dict["ks"])

        # Invalid KS (last 3 digits are not match BIK last 3 digits)
        self.data["ks"] = "30101810500000000218"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn(error_messages["ks_last_3"], e.message_dict["ks"])

        # Invalid KS (first 3 digits are not match sequence "301")
        self.data["ks"] = "30001810500000000219"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn(error_messages["ks_first_3"], e.message_dict["ks"])

        # Invalid KS and valid BIK
        self.data["ks"] = "30101810500000005219"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn(error_messages["check_num_bik"], e.message_dict["ks"])

        # Valid KS and invalid BIK
        self.data["bik"] = "044552219"
        org = self.model(**self.data)
        try:
            org.full_clean()
        except ValidationError as e:
            self.assertTrue(e.message_dict.get("ks", ""))
            self.assertIn(error_messages["check_num_bik"], e.message_dict["ks"])
