from django.contrib.auth.models import (BaseUserManager)
from rest_framework.authtoken.models import Token

"""UserManager class: Interface between the default django user model
                      and the custom user model used in the API."""
class UserManager(BaseUserManager):

    #Constructor
    def __init__(self) -> None:
         #instance attributes.
         super().__init__()

    #create_user: create and save a new user"""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    #create_staffuser: create and save a new staffuser"""
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        user = self.create_user(email, password, **extra_fields)
        return user

    #create_superuser: create and save a new super user"""
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        user = self.create_user(email, password, **extra_fields)
        return user

    #create_token: create a new access token for a user
    def create_token(user):
        token, create = Token.objects.get_or_create(user=user)
        return token.key

    #get_user_by_token: find a user by a token key
    def get_user_by_token(token_key):
        """get the user by token key"""
        try:
            token = Token.objects.get(key=token_key)
            return token.user_id
        except:
            return None