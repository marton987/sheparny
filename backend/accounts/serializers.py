""" Accounts Serializers """
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Account Serializer
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
    token = serializers.SerializerMethodField('get_user_token')

    class Meta:
        model = Account
        fields = (
            'id', 'email', 'username', 'password', 'token'
        )

    @staticmethod
    def get_user_token(account):
        """
        Get token from account instance
        :param account: User account to retrieve token
        :return: String with user token
        """
        token, created = Token.objects.get_or_create(user=account)  # pylint: disable=unused-variable
        return str(token)

    @staticmethod
    def validate_password(value):
        """
        Validates that the provided password is strong
        :param value: String with user's password
        :return: String with valid password
        """
        validate_password(value)
        return value

    @staticmethod
    def validate_email(value):
        """
        Validates that the email is unique
        :param value: String with user's email
        :return: String with user's email
        """
        try:
            Account.objects.get(email=value)
        except Account.DoesNotExist:
            return value
        raise serializers.ValidationError('Account already exists.')

    def create(self, validated_data):
        """
        Override create account serializer to handle user password
        :param validated_data: User validated data
        :return: New account instance
        """
        account = Account.objects.create_user(**validated_data)
        account.save()
        return account
