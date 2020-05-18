""" Accounts views """
from django.contrib.auth import authenticate, login, logout
from rest_framework import mixins, permissions, response, status, views, viewsets

from accounts.permissions import SeeOrCreateAccountPermission
from accounts.serializers import AccountSerializer
from accounts.models import Account


class LoginView(views.APIView):
    """
    Login View
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Authenticate user
        :param request: request made by the user
        :return: Response object with account data
        """
        data = request.data
        email = data.get('email')
        password = data.get('password')

        try:
            account = Account.objects.get(email__iexact=email)
            authenticated_account = authenticate(email=account.email, password=password)

            if authenticated_account:
                login(request, authenticated_account)
                serialized_account = AccountSerializer(authenticated_account)
                data = serialized_account.data
                return response.Response(data)

        except Account.DoesNotExist:
            pass

        return response.Response({
            'status': 'Unauthorized',
            'message': 'Email/password combination invalid'
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    """
    Logout View
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        """
        Unauthenticate user
        :param request: Request made by de user
        :return: Response with empty object
        """
        logout(request)

        return response.Response({}, status=status.HTTP_204_NO_CONTENT)


# pylint: disable=too-many-ancestors
class AccountViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Account Viewset
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (SeeOrCreateAccountPermission,)
