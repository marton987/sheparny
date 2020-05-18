""" Accounts tests """
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import AccountFactory
from accounts.models import Account


class LogoutAccountTestCase(APITestCase):
    """
    Logs out a user tests
    """
    def setUp(self):
        self.account = AccountFactory()

    def test_authenticated_logs_out(self):
        """
        GIVEN An authenticated user
        WHEN sends an empty POST to /auth/logout
        THEN should be unauthenticated
        """
        self.client.force_login(self.account)

        response = self.client.post(
            reverse('logout'),
            json.dumps({}),
            content_type='application/json'
        )
        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'response does not has 204 No Content.')
        self.assertEqual(stored_data, {}, 'response doest not contain an empty string')
        self.assertNotIn('token', stored_data, 'response from {} contains account token'.format(reverse('logout')))

    def test_unauthenticated_logout(self):
        """
        GIVEN An unauthenticated account
        WHEN sends an empty POST to /auth/logout
        THEN should remain unauthenticated
        """
        response = self.client.post(
            reverse('logout'),
            json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'response does not has 204 status.')


class LoginAccountTestCase(APITestCase):
    """
    Logs in a account tests
    """
    def setUp(self):
        self.password = 'password'
        self.account = AccountFactory()
        self.account.set_password(self.password)
        self.account.save()

    def test_authenticate_account(self):
        """
        GIVEN An unauthenticated account
        WHEN sends his credentials on a POST to /auth/login
        THEN should be authenticated
        """
        data = {
            'email': self.account.email,
            'password': self.password
        }
        response = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response does not has 200 OK Status.')
        self.assertIn('token', response.data, 'response does not has an authentication token.')
        self.assertNotIn('password', response.data, 'response contains the password of the account.')

    def test_authenticate_account_non_sensitive(self):
        """
        GIVEN An unauthenticated account
        WHEN sends his credentials on a POST to /auth/login with uppercase
        THEN should be authenticated
        """
        data = {
            'email': self.account.email.upper(),
            'password': self.password
        }
        response = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response does not has 200 OK Status.')

    def test_non_existent_account(self):
        """
        GIVEN An unauthenticated account
        WHEN sends his credentials on a POST to /auth/login with non-existent email
        THEN should not be authenticated
        """
        data = {
            'email': 'invalid@email.com',
            'password': self.password
        }
        response = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'response does not has 401 status.')
        self.assertNotIn('password', response.data, 'response contains the password of the account.')

    def test_invalid_credentials(self):
        """
        GIVEN An unauthenticated account
        WHEN sends invalid credentials on a POST to /auth/login
        THEN should not be authenticated
        """
        data = {
            'email': self.account.email,
            'password': 'Inv4lidPassw0rd!'
        }
        response = self.client.post(
            reverse('login'),
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'response does not has 401 status.')


class AccountTestCase(APITestCase):
    """
    Accounts tests
    """
    def setUp(self):
        self.account = AccountFactory()
        self.account_stub = AccountFactory.stub().__dict__

    def test_get_account_form_string(self):
        """
        GIVEN a developer user
        WHEN prints the account object
        THEN the email should be displayed
        """
        self.assertEqual(str(self.account), self.account.email, 'Account string does not match')

    def test_create_superuser_from_command(self):
        """
        GIVEN a developer user
        WHEN tries to create a superuser from the command line
        THEN the user should be created and be a staff member
        """
        account = Account.objects.create_superuser(**self.account_stub)
        self.assertEqual(account.email, self.account_stub.get('email'), 'created email does not match')
        self.assertTrue(account.is_staff, 'new account is not staff member')

    def test_see_account_unauthenticated(self):
        """
        GIVEN An unauthenticated account
        WHEN tries to see another Account account
        THEN should not be able to see any details
        """
        response = self.client.get(
            reverse('accounts-detail', kwargs={'pk': self.account.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'response does not has 401 status')

    def test_see_another_account_authenticated(self):
        """
        GIVEN An authenticated account
        WHEN tries to see another account account
        THEN should not be able to see any details
        """
        self.client.force_login(self.account)
        account = AccountFactory()
        response = self.client.get(
            reverse('accounts-detail', kwargs={'pk': account.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'response does not has 403 status')

    def test_see_account_authenticated(self):
        """
        GIVEN An authenticated account
        WHEN tries to see his account
        THEN should be able to see his details
        """
        self.client.force_login(self.account)
        response = self.client.get(
            reverse('accounts-detail', kwargs={'pk': self.account.pk}),
        )
        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response does not has 200 status')
        self.assertNotIn('password', stored_data, 'response contains the password of the account.')
        self.assertEqual(self.account.username, stored_data.get('username'),
                         'response does not contains the username of the account')
        self.assertEqual(self.account.email, stored_data.get('email'),
                         'response does not contains the email of the account')

    def test_create_new_account(self):
        """
        GIVEN An unauthenticated account
        WHEN sends his credentials with a strong password on a POST to /api/accounts
        THEN should be created
        """
        data = {
            'email': self.account_stub.get('email'),
            'password': 'Str0ngPassw0rd!'
        }
        response = self.client.post(
            reverse('accounts-list'),
            json.dumps(data),
            content_type='application/json'
        )
        stored_data = response.data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'response does not has 201 OK Status')
        self.assertEqual(self.account_stub.get('email'), stored_data.get('email'),
                         'response does not contains the email of the account')
        self.assertIn(stored_data.get('username'), stored_data.get('email'),
                      'response username should be part of the email')
        self.assertNotIn('password', response.data, 'response contains the password of the account')
        # Account should exist on DB
        count_account = Account.objects.filter(email=self.account_stub.get('email')).count()
        self.assertEqual(count_account, 1, 'account is not in DataBase')

    def test_create_account_soft_password(self):
        """
        GIVEN An unauthenticated account
        WHEN sends credentials with a soft password on a POST to /api/accounts
        THEN should not be created
        """
        data = {
            'email': self.account_stub.get('email'),
            'password': '1234'
        }
        response = self.client.post(
            reverse('accounts-list'),
            json.dumps(data),
            content_type='application/json'
        )
        errors_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'response does not has 400 Error')
        self.assertIn('This password is too common.', errors_data.get('password'), 'password field is not validated')

    def test_create_existing_account(self):
        """
        GIVEN An unauthenticated account
        WHEN sends credentials of an existent account on a POST to /api/accounts
        THEN should not be created
        """
        account = AccountFactory()
        data = {
            'email': account.email,
            'password': 'Str0ngPassw0rd!'
        }
        response = self.client.post(
            reverse('accounts-list'),
            json.dumps(data),
            content_type='application/json'
        )
        errors_data = response.data
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'response does not has 400 Error')
        self.assertIn('Account already exists.', errors_data.get('email'), 'password field is not validated')
