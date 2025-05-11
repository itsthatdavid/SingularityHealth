from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from .utils.encryption import EncryptedCharField
import uuid

class AuditModelMixin(models.Model):
    """
    Mixin para agregar campos de auditoría requeridos por HIPAA
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'AppUser',
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        null=True
    )
    updated_by = models.ForeignKey(
        'AppUser',
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        null=True
    )
    is_deleted = models.BooleanField(default=False)  # Soft delete
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

# Validators
phone_validator = RegexValidator(
    regex=r'^\d+$',
    message='El número de teléfono debe contener solo dígitos'
)

address_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9\s\-N*]+$',
    message='La dirección solo puede contener letras, números, espacios y los caracteres - N *'
)

class Country(models.Model, AuditModelMixin):
    country_code = models.CharField(max_length=4, unique=True)
    country_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'Country_TB'

    def __str__(self):
        return self.country_name

class TypeDocument(models.Model, AuditModelMixin):
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

class AppUser(AbstractBaseUser, PermissionsMixin, AuditModelMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_temporal = models.BooleanField(default=False)
    is_militar = models.BooleanField(default=False)
    time_create = models.DateTimeField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    # Campos encriptados
    _ssn = models.CharField(max_length=255, null=True, blank=True)  # Número de seguro social encriptado
    ssn = EncryptedCharField('_ssn')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'name']

    class Meta:
        db_table = 'AppUser_TB'

    def __str__(self):
        return self.email

class UserDocument(AuditModelMixin):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    type_document = models.ForeignKey(TypeDocument, on_delete=models.PROTECT)
    _document = models.CharField(max_length=255)  # Campo encriptado
    document = EncryptedCharField('_document')
    place_expedition = models.CharField(max_length=60)
    date_expedition = models.DateField()

    class Meta:
        db_table = 'UserDocument_TB'
        unique_together = ['type_document', '_document']

    def __str__(self):
        return f"{self.user.email} - {self.document}"

class ContactInfo(AuditModelMixin):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    _address = models.CharField(max_length=255)  # Campo encriptado
    address = EncryptedCharField('_address')
    city = models.CharField(max_length=50)
    _phone = models.CharField(max_length=255)  # Campo encriptado
    phone = EncryptedCharField('_phone')
    _cel_phone = models.CharField(max_length=255)  # Campo encriptado
    cel_phone = EncryptedCharField('_cel_phone')
    _emergency_name = models.CharField(max_length=255)  # Campo encriptado
    emergency_name = EncryptedCharField('_emergency_name')
    _emergency_phone = models.CharField(max_length=255)  # Campo encriptado
    emergency_phone = EncryptedCharField('_emergency_phone')

    class Meta:
        db_table = 'ContactInfo_TB'

    def __str__(self):
        return f"{self.user.email} - {self.city}"

# Modelo para registro de auditoría HIPAA
class AuditLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AppUser, on_delete=models.PROTECT)
    action = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    success = models.BooleanField()
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'AuditLog_TB'
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['user']),
            models.Index(fields=['action']),
            models.Index(fields=['resource_type']),
        ]