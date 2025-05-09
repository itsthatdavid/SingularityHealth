from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
    last_name = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_temporal = models.BooleanField(default=False)
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
    document = models.CharField(max_length=20)
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
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    cel_phone = models.CharField(max_length=20)
    emergency_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'ContactInfo_TB'

    def __str__(self):
        return f"{self.user.email} - {self.city}"