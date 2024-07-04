from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username,email,full_name,birthday,password,profile="blank-profile-picture.png"):
        if not username :
            raise ValueError('user must have user_name')
        if not email :
            raise ValueError('user must have email')
        if not full_name :
            raise ValueError('user must have full_name')
        if not birthday :
            raise ValueError('user must birthday')
        
        user = self.model(username = username,profile=profile,email=self.normalize_email(email),full_name=full_name,birthday=birthday)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,email,full_name,password):
        user =self.create_user(username,email,full_name,password)
        user.is_admin = True 
        user.save(using=self._db)
        return user