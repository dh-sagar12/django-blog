
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random

# from core.models import BranchModel
# Create your models here.



class CustomAccountManager(BaseUserManager):
    def create_user(self,  email, first_name,  last_name, password=None, gender='O'):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name = last_name, 
            gender  =  gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

        
    def create_superuser(self, email, first_name, last_name, password ):

        user=  self.create_user( email=email,first_name=first_name, last_name=last_name,  password=password)

        user.is_staff =  True
        user.is_superuser =  True
        user.is_active =  True
        user.save()
        
        if user.is_superuser is not True:
            raise ValueError('Superuser must be assigned to is_superuser True')

        
        if user.is_staff is not True:
            raise ValueError('Superuser must be assigned to is_staff True')
    
    
class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    email= models.EmailField(_("email address"), max_length=254, unique=True)
    username =  models.CharField(_("username"), max_length=20, unique=True, auto_created=True)
    first_name= models.CharField(max_length=100, null=False)
    middle_name = models.CharField(max_length=100, blank= True, null=True)
    last_name =  models.CharField(max_length=100, null=False)
    date_of_birth =  models.DateField(blank=True, null=True)
    password =  models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)
    date_joined = models.DateTimeField(blank=True, default=timezone.now)
    avatar = models.ImageField(upload_to='Avatars/',  blank=True)

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_OTHER, 'Other')]
    gender = models.CharField(choices=GENDER_CHOICES, max_length=5, null=False, blank=False)
    
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table=  'users'

    def save(self, *args, **kwargs):  # new
        if self.username == '' or self.username is None:
            random_int  = random.randint(100, 1000)
            self.username = f"{self.first_name}{random_int}"
        return super().save(*args, **kwargs)


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id')
    token =  models.CharField(max_length=200, null=False, blank=False)
    expired =  models.BooleanField(default=False, null=False)
    created_on  = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tokens'
    
    def __str__(self) -> str:
        return self.token