import graphene
from graphene_django import DjangoObjectType
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

# Validators
phone_validator = RegexValidator(
    regex=r'^\d+$',
    message='El número de teléfono debe contener solo dígitos'
)

address_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s\-N*]+$',  # Cambiado para incluir N
    message='La dirección solo puede contener letras, números, espacios y los caracteres - N *'
)

class Country(models.Model):
    country_code = models.CharField(max_length=4, unique=True)
    country_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Country_TB'

    def __str__(self):
        return self.country_name

class TypeDocument(models.Model):
    name_type_document = models.CharField(max_length=50)

    class Meta:
        db_table = 'TypeDocument_TB'

    def __str__(self):
        return self.name_type_document

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # Campo añadido explícitamente
    last_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_temporal = models.BooleanField(default=False)
    is_militar = models.BooleanField(default=False)  # Nuevo campo
    time_create = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'name']

    class Meta:
        db_table = 'AppUser_TB'

    def __str__(self):
        return self.email

class UserDocument(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    type_document = models.ForeignKey(TypeDocument, on_delete=models.PROTECT)
    document = models.CharField(
        max_length=20,
        blank=True,  # Permite espacios en blanco (w)
        help_text='Número de documento'
    )
    place_expedition = models.CharField(max_length=60)
    date_expedition = models.DateField()

    class Meta:
        db_table = 'UserDocument_TB'
        unique_together = ['type_document', 'document']

    def __str__(self):
        return f"{self.user.email} - {self.document}"

class ContactInfo(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    address = models.CharField(
        max_length=60,
        validators=[address_validator],
        help_text='Dirección (puede contener letras, números, espacios y los caracteres - N *)'
    )
    city = models.CharField(max_length=50)
    phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text='Número de teléfono (solo dígitos)'
    )
    cel_phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text='Número de celular (solo dígitos)'
    )
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(
        max_length=20,
        validators=[phone_validator],
        help_text='Número de teléfono de emergencia (solo dígitos)'
    )

    class Meta:
        db_table = 'ContactInfo_TB'

    def __str__(self):
        return f"{self.user.email} - {self.city}"

class RegisterUser(graphene.Mutation):
    class Arguments:
        # User fields
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        last_name = graphene.String(required=True)
        name = graphene.String(required=True)
        is_militar = graphene.Boolean(required=True)
        
        # Document fields
        type_document_id = graphene.ID(required=True)
        document = graphene.String(required=True)
        place_expedition = graphene.String(required=True)
        date_expedition = graphene.String(required=True)
        
        # Contact fields
        country_id = graphene.ID(required=True)
        address = graphene.String(required=True)
        city = graphene.String(required=True)
        phone = graphene.String(required=True)
        cel_phone = graphene.String(required=True)
        emergency_name = graphene.String(required=True)
        emergency_phone = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            # Create user first
            user = AppUser.objects.create_user(
                email=kwargs.get('email'),
                username=kwargs.get('username'),
                password=kwargs.get('password'),
                last_name=kwargs.get('last_name'),
                name=kwargs.get('name'),
                is_militar=kwargs.get('is_militar')
            )

            # Create document
            UserDocument.objects.create(
                user=user,
                type_document_id=kwargs.get('type_document_id'),
                document=kwargs.get('document'),
                place_expedition=kwargs.get('place_expedition'),
                date_expedition=kwargs.get('date_expedition')
            )

            # Create contact info
            ContactInfo.objects.create(
                user=user,
                country_id=kwargs.get('country_id'),
                address=kwargs.get('address'),
                city=kwargs.get('city'),
                phone=kwargs.get('phone'),
                cel_phone=kwargs.get('cel_phone'),
                emergency_name=kwargs.get('emergency_name'),
                emergency_phone=kwargs.get('emergency_phone')
            )

            return RegisterUser(success=True, message="Usuario registrado exitosamente")
        except Exception as e:
            return RegisterUser(success=False, message=str(e))