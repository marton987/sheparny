""" Accounts models """
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class AccountManager(BaseUserManager):
    """ Account Manager"""
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        :param email: String with user's email
        :param password: String with user's password
        :return: Account instance
        """
        account = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        :param email: String with user's email
        :param password: String with user's password
        :return: Account instance
        """
        account = self.create_user(email, password=password, **kwargs)
        account.is_staff = True
        account.save()
        return account


class Account(AbstractBaseUser):
    """ Account model """
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    username = models.CharField(verbose_name='username', max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """ Email string """
        return self.email

    def save(self, *args, **kwargs):
        """ Override save method """
        # According requirements username is the first part of the email
        self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
