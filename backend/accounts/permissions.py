""" Accounts permissions """
from rest_framework import permissions


class SeeOrCreateAccountPermission(permissions.BasePermission):
    """
    Returns true if the request.Account is owner of the account
    """
    def has_permission(self, request, view):
        """
        Returns true or false if the Account has the permission
        :param request: Request made by the Account
        :param view: View set
        :return: Boolean with the Account permission
        """
        if view.action == 'create':
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Returns `True` if permission is granted, `False` otherwise.
        """
        return obj == request.user
