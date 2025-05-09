import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import UserDocument, ContactInfo, Country, TypeDocument
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.core.exceptions import ValidationError
import bcrypt

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
                 'time_create', 'email_verified')

class UserDocumentType(DjangoObjectType):
    class Meta:
        model = UserDocument
        fields = '__all__'

class ContactInfoType(DjangoObjectType):
    class Meta:
        model = ContactInfo
        fields = '__all__'

class UserRegistrationInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    last_name = graphene.String(required=True)
    name = graphene.String(required=True)
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

class RegisterUser(graphene.Mutation):
    class Arguments:
        input = UserRegistrationInput(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    @staticmethod
    def mutate(root, info, input):
        try:
            # Validar si el usuario ya existe
            User = get_user_model()
            if User.objects.filter(email=input.email).exists():
                raise ValidationError('El email ya está registrado')
            if User.objects.filter(username=input.username).exists():
                raise ValidationError('El nombre de usuario ya está registrado')

            # Crear usuario
            user = User.objects.create_user(
                email=input.email,
                username=input.username,
                password=input.password,
                last_name=input.last_name,
                name=input.name
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
                message='Error al registrar el usuario'
            )

class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    all_countries = graphene.List(CountryType)
    all_document_types = graphene.List(TypeDocumentType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

    def resolve_all_countries(self, info):
        return Country.objects.all()

    def resolve_all_document_types(self, info):
        return TypeDocument.objects.all()

class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)