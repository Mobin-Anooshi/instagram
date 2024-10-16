from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.



class User(AbstractBaseUser):
    username = models.CharField(max_length=200,unique=True)
    profile = models.ImageField(upload_to='profile_image',default='blank-profile-picture.png')
    bio = models.CharField(max_length=300,blank=True ,null=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    birthday = models.DateField(blank= True ,null=True)
    privet = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','full_name']
    
    def __str__ (self):
        return self.username 
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_lable):
        return True
    
    def folowerscount(self):
        return self.followers.count()
    
    def folowingcount(self):
        return self.following.count()
    
    @property
    def is_staff(self):
        return self.is_admin