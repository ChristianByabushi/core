from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='images/avatar/', default='/images/avatar/avatar.png')
    objects = CustomUserManager()
    role = models.CharField(max_length=50, default='visiteur',choices=[('admin', 'admin'), ('visiteur', 'visiteur'),('locataire', 'locataire'),('gestionnaire', 'gestionnaire')]) 
    USERNAME_FIELD = 'email'
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
       
    def __str__(self):
        return f"{self.id}-{self.email}"
    
    
from django.db import models
from user.models import User
from user.models import User
class Locataire(User):
    numeroTel = models.CharField(max_length=30, null=True)
    adresse = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
       
    def __str__(self):
        return f"Locataire-{self.first_name}-{self.last_name}.{self.id}"

    @classmethod
    def total_locataires(cls):
        return cls.objects.count() 