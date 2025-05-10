import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import UserDocument, ContactInfo, Country, TypeDocument
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import bcrypt

# Types
class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = '__all__'

class TypeDocumentType(DjangoObjectType):
    class Meta:
        model = TypeDocument
        fields = '__all__'

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'last_name', 'name', 'is_active', 
                 'is_temporal', 'is_militar', 'time_create', 'email_verified')

class UserDocumentType(DjangoObjectType):
    class Meta:
        model = UserDocument
        fields = '__all__'

class ContactInfoType(DjangoObjectType):
    class Meta:
        model = ContactInfo
        fields = '__all__'

# Inputs
class UserRegistrationInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    last_name = graphene.String(required=True)
    name = graphene.String(required=True)
    is_militar = graphene.Boolean(required=True)
    document_type = graphene.ID(required=True)
    document_number = graphene.String(required=True)
    document_expedition_place = graphene.String(required=True)
    document_expedition_date = graphene.Date(required=True)
    country = graphene.ID(required=True)
    address = graphene.String(required=True)
    city = graphene.String(required=True)
    phone = graphene.String(required=True)
    cel_phone = graphene.String(required=True)
    emergency_name = graphene.String(required=True)
    emergency_phone = graphene.String(required=True)

# Mutations
class CreateTypeDocument(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    type_document = graphene.Field(TypeDocumentType)
    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, name):
        try:
            if TypeDocument.objects.filter(name_type_document=name).exists():
                return CreateTypeDocument(
                    success=False,
                    message=f"Ya existe un tipo de documento con el nombre: {name}"
                )

            type_document = TypeDocument.objects.create(
                name_type_document=name
            )

            return CreateTypeDocument(
                type_document=type_document,
                success=True,
                message="Tipo de documento creado exitosamente"
            )
        except Exception as e:
            return CreateTypeDocument(
                success=False,
                message=str(e)
            )

class CreateCountry(graphene.Mutation):
    class Arguments:
        country_code = graphene.String(required=True)
        country_name = graphene.String(required=True)

    country = graphene.Field(CountryType)
    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, country_code, country_name):
        try:
            if Country.objects.filter(country_code=country_code).exists():
                return CreateCountry(
                    success=False,
                    message=f"Ya existe un país con el código: {country_code}"
                )

            country = Country.objects.create(
                country_code=country_code,
                country_name=country_name
            )

            return CreateCountry(
                country=country,
                success=True,
                message="País creado exitosamente"
            )
        except Exception as e:
            return CreateCountry(
                success=False,
                message=str(e)
            )

class RegisterUser(graphene.Mutation):
    class Arguments:
        input = UserRegistrationInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, input):
        try:
            # Validaciones de campos específicos
            address_validator = RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-N*]+$',
                message='La dirección solo puede contener letras, números, espacios y los caracteres - N *'
            )
            phone_validator = RegexValidator(
                regex=r'^\d+$',
                message='El número de teléfono debe contener solo dígitos'
            )

            # Validar formato de dirección y teléfonos
            address_validator(input.address)
            phone_validator(input.phone)
            phone_validator(input.cel_phone)
            phone_validator(input.emergency_phone)

            # Validar si el usuario ya existe
            User = get_user_model()
            if User.objects.filter(email=input.email).exists():
                raise ValidationError('El email ya está registrado')
            if User.objects.filter(username=input.username).exists():
                raise ValidationError('El nombre de usuario ya está registrado')

            # Validar si existe el tipo de documento
            if not TypeDocument.objects.filter(id=input.document_type).exists():
                raise ValidationError('El tipo de documento no existe')

            # Validar si existe el país
            if not Country.objects.filter(id=input.country).exists():
                raise ValidationError('El país no existe')

            # Crear usuario
            user = User.objects.create_user(
                email=input.email,
                username=input.username,
                password=input.password,
                last_name=input.last_name,
                name=input.name,
                is_militar=input.is_militar
            )

            # Crear documento de usuario
            UserDocument.objects.create(
                user=user,
                type_document_id=input.document_type,
                document=input.document_number,
                place_expedition=input.document_expedition_place,
                date_expedition=input.document_expedition_date
            )

            # Crear información de contacto
            ContactInfo.objects.create(
                user=user,
                country_id=input.country,
                address=input.address,
                city=input.city,
                phone=input.phone,
                cel_phone=input.cel_phone,
                emergency_name=input.emergency_name,
                emergency_phone=input.emergency_phone
            )

            return RegisterUser(
                user=user,
                success=True,
                message='Usuario registrado exitosamente'
            )

        except ValidationError as e:
            return RegisterUser(
                success=False,
                message=str(e)
            )
        except Exception as e:
            return RegisterUser(
                success=False,
                message=str(e)
            )

# Query
class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    all_countries = graphene.List(CountryType)
    all_document_types = graphene.List(TypeDocumentType)
    country_by_id = graphene.Field(CountryType, id=graphene.ID(required=True))
    document_type_by_id = graphene.Field(TypeDocumentType, id=graphene.ID(required=True))

    @login_required
    def resolve_me(self, info):
        return info.context.user

    def resolve_all_countries(self, info):
        return Country.objects.all()

    def resolve_all_document_types(self, info):
        return TypeDocument.objects.all()

    def resolve_country_by_id(self, info, id):
        try:
            return Country.objects.get(pk=id)
        except Country.DoesNotExist:
            return None

    def resolve_document_type_by_id(self, info, id):
        try:
            return TypeDocument.objects.get(pk=id)
        except TypeDocument.DoesNotExist:
            return None

# Mutation
class Mutation(graphene.ObjectType):
    create_type_document = CreateTypeDocument.Field()
    create_country = CreateCountry.Field()
    register_user = RegisterUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)