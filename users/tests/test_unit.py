from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Country, TypeDocument, ContactInfo, AppUser, UserDocument
from datetime import date

class ModelUnitTests(TestCase):
    """Pruebas unitarias para los modelos"""
    
    def setUp(self):
        self.country = Country.objects.create(
            country_code="CO",
            country_name="Colombia"
        )
        self.doc_type = TypeDocument.objects.create(
            name_type_document="Cédula de Ciudadanía"
        )
        self.user = AppUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",
            name="Test",
            last_name="User",
            is_militar=False
        )

    def test_country_creation(self):
        self.assertEqual(str(self.country), "Colombia")
        self.assertEqual(self.country.country_code, "CO")

    def test_type_document_creation(self):
        self.assertEqual(str(self.doc_type), "Cédula de Ciudadanía")

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_militar)

    def test_user_document_creation(self):
        user_doc = UserDocument.objects.create(
            user=self.user,
            type_document=self.doc_type,
            document="1234567890",
            place_expedition="Bogotá",
            date_expedition=date(2020, 1, 1)
        )
        self.assertEqual(str(user_doc), f"{self.user.email} - 1234567890")

    def test_contact_info_creation(self):
        contact = ContactInfo.objects.create(
            user=self.user,
            country=self.country,
            address="Calle 123 N 45-67",
            city="Bogotá",
            phone="1234567",
            cel_phone="3001234567",
            emergency_name="Emergency Contact",
            emergency_phone="3009876543"
        )
        self.assertEqual(str(contact), f"{self.user.email} - Bogotá")

    def test_phone_validator(self):
        with self.assertRaises(ValidationError):
            contact = ContactInfo(
                user=self.user,
                country=self.country,
                address="Calle 123",
                city="Bogotá",
                phone="123abc",  # Inválido
                cel_phone="3001234567",
                emergency_name="Emergency Contact",
                emergency_phone="3009876543"
            )
            contact.full_clean()

    def test_address_validator(self):
        with self.assertRaises(ValidationError):
            contact = ContactInfo(
                user=self.user,
                country=self.country,
                address="Calle 123 @#$%",  # Inválido
                city="Bogotá",
                phone="1234567",
                cel_phone="3001234567",
                emergency_name="Emergency Contact",
                emergency_phone="3009876543"
            )
            contact.full_clean()

class UserManagerUnitTests(TestCase):
    """Pruebas unitarias para el UserManager"""

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            AppUser.objects.create_user(email="", password="test123")

    def test_create_user_normalizes_email(self):
        user = AppUser.objects.create_user(
            email="TEST@Example.Com",
            password="test123",
            username="test",
            name="Test",
            last_name="User"
        )
        self.assertEqual(user.email, "TEST@example.com")

    def test_create_superuser(self):
        user = AppUser.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            username="admin",
            name="Admin",
            last_name="User"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)