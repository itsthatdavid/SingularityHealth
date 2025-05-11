from django.test import TestCase
from graphene.test import Client
from ..models import Country, TypeDocument, AppUser
from singularity.schema import schema
from datetime import date

class GraphQLIntegrationTests(TestCase):
    """Pruebas de integración para GraphQL"""

    def setUp(self):
        self.client = Client(schema)
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
        self.assertEqual(
            response['data']['createCountry']['country']['countryName'],
            "United States"
        )

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
        self.assertEqual(
            response['data']['createTypeDocument']['typeDocument']['nameTypeDocument'],
            "Pasaporte"
        )

    def test_complete_user_registration_flow(self):
        """Prueba el flujo completo de registro de usuario"""
        result = self._register_user("test@example.com")
        self.assertTrue(result['success'])
        
        # Verificar que se creó el usuario
        user = AppUser.objects.get(email="test@example.com")
        self.assertTrue(user.is_active)
        
        # Verificar documento
        self.assertTrue(user.userdocument_set.exists())
        
        # Verificar información de contacto
        self.assertTrue(user.contactinfo_set.exists())

    def test_user_registration_with_existing_email(self):
        # Primer registro
        self._register_user("duplicate@example.com")
        
        # Intentar registro con el mismo email
        result = self._register_user("duplicate@example.com")
        self.assertFalse(result['success'])
        self.assertIn("email ya está registrado", result['message'])

    def test_user_registration_with_invalid_data(self):
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
                "email": "invalid-email",  # Email inválido
                "username": "",  # Username vacío
                "password": "123",  # Contraseña muy corta
                "lastName": "User",
                "name": "Test",
                "isMilitar": False,
                "documentType": "999",  # ID que no existe
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
        self.assertFalse(response['data']['registerUser']['success'])

    def _register_user(self, email):
        """Helper method para registrar usuarios"""
        mutation = '''
            mutation($input: UserRegistrationInput!) {
                registerUser(input: $input) {
                    success
                    message
                    user { id email }
                }
            }
        '''
        variables = {
            "input": {
                "email": email,
                "username": f"user_{email.split('@')[0]}",
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
        response = self.client.execute(mutation, variables=variables)
        return response['data']['registerUser']