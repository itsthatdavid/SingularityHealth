from django.test import TestCase
from graphene.test import Client
from ..models import Country, TypeDocument
from singularity.schema import schema

class GraphQLAPITests(TestCase):
    """Pruebas para la API GraphQL"""

    def setUp(self):
        self.client = Client(schema)
        self.country = Country.objects.create(
            country_code="CO",
            country_name="Colombia"
        )
        self.doc_type = TypeDocument.objects.create(
            name_type_document="Cédula de Ciudadanía"
        )

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
        self.assertEqual(
            response['data']['allCountries'][0]['countryName'],
            "Colombia"
        )

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
        self.assertEqual(
            response['data']['allDocumentTypes'][0]['nameTypeDocument'],
            "Cédula de Ciudadanía"
        )

    def test_query_country_by_id(self):
        query = '''
            query($id: ID!) {
                countryById(id: $id) {
                    id
                    countryName
                }
            }
        '''
        variables = {"id": str(self.country.id)}
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(
            response['data']['countryById']['countryName'],
            "Colombia"
        )

    def test_query_document_type_by_id(self):
        query = '''
            query($id: ID!) {
                documentTypeById(id: $id) {
                    id
                    nameTypeDocument
                }
            }
        '''
        variables = {"id": str(self.doc_type.id)}
        response = self.client.execute(query, variables=variables)
        self.assertIsNone(response.get('errors'))
        self.assertEqual(
            response['data']['documentTypeById']['nameTypeDocument'],
            "Cédula de Ciudadanía"
        )