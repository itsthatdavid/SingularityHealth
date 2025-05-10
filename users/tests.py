from django.test import TestCase
from django.core.exceptions import ValidationError
from graphene.test import Client
from django.contrib.auth import get_user_model
from .models import Country, TypeDocument, UserDocument, ContactInfo
from singularity.schema import schema
import json
from datetime import date

class ModelsTestCase(TestCase):
    def setUp(self):
        # Crear país de prueba
        self.country = Country.objects.create(
            country_code="CO",
            country_name="Colombia"
        )

        # Crear tipo de documento de prueba
        self.doc_type = TypeDocument.objects.create(
            name_type_document="Cédula de Ciudadanía"
        )

        # Crear usuario de prueba
        self.user = get_user_model().objects.create_user(
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

    def test_invalid_phone_number(self):
        with self.assertRaises(ValidationError):
            contact = ContactInfo(
                user=self.user,
                country=self.country,
                address="Calle 123",
                city="Bogotá",
                phone="123abc",  # Número inválido
                cel_phone="3001234567",
                emergency_name="Emergency Contact",
                emergency_phone="3009876543"
            )
            contact.full_clean()  # Esto dispara la validación

    def test_invalid_address(self):
        with self.assertRaises(ValidationError):
            contact = ContactInfo(
                user=self.user,
                country=self.country,
                address="Calle 123 @#$%",  # Dirección inválida
                city="Bogotá",
                phone="1234567",
                cel_phone="3001234567",
                emergency_name="Emergency Contact",
                emergency_phone="3009876543"
            )
            contact.full_clean()  # Esto dispara la validación

class GraphQLTestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)
        # Crear datos de prueba
        self.country = Country.objects.create(
            country_code="CO",
            country_name="Colombia"
        )
        self.doc_type = TypeDocument.objects.create(
            name_type_document="Cédula de Ciudadanía"
        )

    def test_create_country_mutation(self):
        mutation = '''
            mutation {
                createCountry(countryCode: "US", countryName: "United States") {
                    success
                    message
                    country {
                        id
                        countryCode
                        countryName
                    }
                }
            }
        '''
        response = self.client.execute(mutation)
        self.assertIsNone(response.get('errors'))
        self.assertTrue(response['data']['createCountry']['success'])
        self.assertEqual(response['data']['createCountry']['country']['countryName'], "United States")

    def test_create_document_type_mutation(self):
        mutation = '''
            mutation {
                createTypeDocument(name: "Pasaporte") {
                    success
                    message
                    typeDocument {
                        id
                        nameTypeDocument
                    }
                }
            }
        '''
        response = self.client.execute(mutation)
        self.assertIsNone(response.get('errors'))
        self.assertTrue(response['data']['createTypeDocument']['success'])
        self.assertEqual(response['data']['createTypeDocument']['typeDocument']['nameTypeDocument'], "Pasaporte")

    def test_register_user_mutation(self):
        mutation = '''
            mutation($input: UserRegistrationInput!) {
                registerUser(input: $input) {
                    success
                    message
                    user {
                        id
                        email
                        username
                    }
                }
            }
        '''
        variables = {
            "input": {
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "testpass123",
                "lastName": "User",
                "name": "New",
                "isMilitar": False,
                "documentType": str(self.doc_type.id),
                "documentNumber": "1234567890",
                "documentExpeditionPlace": "Bogotá",
                "documentExpeditionDate": "2020-01-01",
                "country": str(self.country.id),
                "address": "Calle 123 N 45-67",
                "city": "Bogotá",
                "phone": "1234567",
                "celPhone": "3001234567",
                "emergencyName": "Emergency Contact",
                "emergencyPhone": "3009876543"
            }
        }
        response = self.client.execute(mutation, variables=variables)
        self.assertIsNone(response.get('errors'))
        self.assertTrue(response['data']['registerUser']['success'])
        self.assertEqual(response['data']['registerUser']['user']['email'], "newuser@example.com")

    def test_query_all_countries(self):
        query = '''
            query {
                allCountries {
                    id
                    countryCode
                    countryName
                }
            }
        '''
        response = self.client.execute(query)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(len(response['data']['allCountries']), 1)
        self.assertEqual(response['data']['allCountries'][0]['countryName'], "Colombia")

    def test_query_all_document_types(self):
        query = '''
            query {
                allDocumentTypes {
                    id
                    nameTypeDocument
                }
            }
        '''
        response = self.client.execute(query)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(len(response['data']['allDocumentTypes']), 1)
        self.assertEqual(response['data']['allDocumentTypes'][0]['nameTypeDocument'], "Cédula de Ciudadanía")

    def test_duplicate_email_registration(self):
        mutation = '''
            mutation($input: UserRegistrationInput!) {
                registerUser(input: $input) {
                    success
                    message
                }
            }
        '''
        variables = {
            "input": {
                "email": "duplicate@example.com",
                "username": "user1",
                "password": "testpass123",
                "lastName": "User",
                "name": "Test",
                "isMilitar": False,
                "documentType": str(self.doc_type.id),
                "documentNumber": "1234567890",
                "documentExpeditionPlace": "Bogotá",
                "documentExpeditionDate": "2020-01-01",
                "country": str(self.country.id),
                "address": "Calle 123 N 45-67",
                "city": "Bogotá",
                "phone": "1234567",
                "celPhone": "3001234567",
                "emergencyName": "Emergency Contact",
                "emergencyPhone": "3009876543"
            }
        }
        
        # Primera ejecución (debería ser exitosa)
        response1 = self.client.execute(mutation, variables=variables)
        self.assertTrue(response1['data']['registerUser']['success'])

        # Cambiar username pero mantener el mismo email
        variables['input']['username'] = "user2"
        
        # Segunda ejecución (debería fallar por email duplicado)
        response2 = self.client.execute(mutation, variables=variables)
        self.assertFalse(response2['data']['registerUser']['success'])
        self.assertIn("email ya está registrado", response2['data']['registerUser']['message'])