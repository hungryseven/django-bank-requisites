from django.test import TestCase
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from test_project.test_app.models import OrganizationUnvalidated
from test_project.test_app.serializers import UnvalidatedModelSerializer, ValidatedModelSerializer
from django_bank_requisites.django_validators import error_messages

class SetUpMixin:
    
    def setUp(self):
        self.data = {
            "organization_name": "ООО ‟ГидроТеплоСервис‟",
            "legal_address": "107078, г Москва, пер. Б.Козловский, дом 5, стр.2",
            "inn": "7701992807",
            "kpp": "770101001",
            "rs": "40702810100020002772",
            "ks": "30101810000000000201",
            "bik": "044525201",
            "bank_name": "ПАО АКБ ‟Авангард‟"
        }

class BankDetailsUnvalidatedModelSerializerTestCase(SetUpMixin, TestCase):
    """
    Tests for model serializer which is used unvalidated abstract bank details model.
    This serializer has all validation on it's own level.
    """
    
    def setUp(self):
        super().setUp()
        self.serializer = UnvalidatedModelSerializer

    def test_serializer_with_valid_data(self):
        serializer = self.serializer(data=self.data)
        flag = True
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            flag = False
        self.assertTrue(flag)
        orgs_count = OrganizationUnvalidated.objects.count()
        self.assertEqual(orgs_count, 1)

    def test_serializer_legal_address_validation(self):
        # Blank legal_address
        self.data["legal_address"] = ""
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("legal_address", ""))
            self.assertIn("This field may not be blank.", serializer.errors["legal_address"])

        # Invalid legal_address length
        self.data["legal_address"] = "0" * 256
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("legal_address", ""))

    def test_serializer_bank_name_validation(self):
        # Blank legal_address
        self.data["bank_name"] = ""
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("bank_name", ""))
            self.assertIn("This field may not be blank.", serializer.errors["bank_name"])

        # Invalid bank_name length
        self.data["bank_name"] = "0" * 256
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("bank_name", ""))

    def test_serializer_inn_validation(self):
        # Blank INN
        self.data["inn"] = ""
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("inn", ""))
            self.assertIn("This field may not be blank.", serializer.errors["inn"])

        # Invalid INN length
        self.data["inn"] = "770199280"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("inn", ""))
            self.assertIn(error_messages["length"], serializer.errors["inn"])

        # Invalid INN structure
        self.data["inn"] = "770199280q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("inn", ""))
            self.assertIn(error_messages["structure"], serializer.errors["inn"])

        # Invalid INN length and structure
        self.data["inn"] = "7701992807q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("inn", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), serializer.errors["inn"])

        # Invalid INN
        self.data["inn"] = "7701992806"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("inn", ""))
            self.assertIn(error_messages["check_num"], serializer.errors["inn"])

    def test_serializer_kpp_validation(self):
        # Blank KPP
        self.data["kpp"] = ""
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("kpp", ""))
            self.assertIn("This field may not be blank.", serializer.errors["kpp"])

        # Invalid KPP length
        self.data["kpp"] = "7701010011"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("kpp", ""))
            self.assertIn(error_messages["length"], serializer.errors["kpp"])

        # Invalid KPP structure
        self.data["kpp"] = "77010100q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("kpp", ""))
            self.assertIn(error_messages["structure"], serializer.errors["kpp"])

        # Invalid KPP length and structure
        self.data["kpp"] = "770101001q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("kpp", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), serializer.errors["kpp"])

    def test_serializer_bik_validation(self):
        # Blank BIK
        self.data["bik"] = ""
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("bik", ""))
            self.assertIn("This field may not be blank.", serializer.errors["bik"])

        # Invalid BIK length
        self.data["bik"] = "04452520"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("bik", ""))
            self.assertIn(error_messages["length"], serializer.errors["bik"])

        # Invalid BIK structure
        self.data["bik"] = "04452520q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("bik", ""))
            self.assertIn(error_messages["structure"], serializer.errors["bik"])

        # Invalid BIK length and structure
        self.data["bik"] = "044525201q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("bik", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), serializer.errors["bik"])

    def test_serializer_rs_validation(self):
        # Blank RS
        self.data["rs"] = ""
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("rs", ""))
            self.assertIn("This field may not be blank.", serializer.errors["rs"])

        # Invalid RS length
        self.data["rs"] = "407028101000200027721"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("rs", ""))
            self.assertIn(error_messages["length"], serializer.errors["rs"])

        # Invalid RS structure
        self.data["rs"] = "4070281010002000277q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("rs", ""))
            self.assertIn(error_messages["structure"], serializer.errors["rs"])

        # Invalid RS length and structure
        self.data["rs"] = "40702810100020002772q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("rs", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), serializer.errors["rs"])

        # Invalid RS and valid BIK
        self.data["rs"] = "40702810100020002771"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("rs", ""))
            self.assertIn(error_messages["check_num_bik"], serializer.errors["rs"])

        # Valid RS and invalid BIK
        self.data["bik"] = "044525200"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("rs", ""))
            self.assertIn(error_messages["check_num_bik"], serializer.errors["rs"])

    def test_serializer_ks_validation(self):
        # Invalid KS length
        self.data["ks"] = "3010181000000000020"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn(error_messages["length"], serializer.errors["ks"])

        # Invalid KS structure
        self.data["ks"] = "3010181000000000020q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn(error_messages["structure"], serializer.errors["ks"])

        # Invalid KS length and structure
        self.data["ks"] = "30101810000000000201q"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn((error_messages["length"] and error_messages["structure"]), serializer.errors["ks"])

        # Invalid KS (last 3 digits are not match BIK last 3 digits)
        self.data["ks"] = "30101810000000000200"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn(error_messages["ks_last_3"], serializer.errors["ks"])

        # Invalid KS (first 3 digits are not match sequence "301")
        self.data["ks"] = "30001810000000000201"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn(error_messages["ks_first_3"], serializer.errors["ks"])

        # Invalid KS and valid BIK
        self.data["ks"] = "30101810000000001201"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn(error_messages["check_num_bik"], serializer.errors["ks"])

        # Valid KS and invalid BIK
        self.data["bik"] = "044526201"
        serializer = self.serializer(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except DRFValidationError:
            self.assertTrue(serializer.errors.get("ks", ""))
            self.assertIn(error_messages["check_num_bik"], serializer.errors["ks"])

class BankDetailsValidatedModelSerializerTestCase(SetUpMixin, TestCase):
    """
    Tests for model serializer which is used validated abstract bank details model.
    This serializer has validation on model level.
    """

    def setUp(self):
        super().setUp()
        self.serializer = ValidatedModelSerializer

    def test_serializer_catches_django_validation_error(self):
        """
        If we want to implement all validation logic on model level
        including clean() method, then DRF won't catch DjangoValidationError
        from model clean() method without custom error handler.
        The result will be a 500 error in server responce.
        """

        # Last 3 digits of the KS compares last 3 digits of the BIK
        # in model clean() method
        self.data["ks"] = "30101810000000000200"
        serializer = self.serializer(data=self.data)
        flag = True
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save() # We will catch DjangoValidationError here
        except DRFValidationError:
            pass
        except DjangoValidationError:
            flag = False
        self.assertFalse(flag)
