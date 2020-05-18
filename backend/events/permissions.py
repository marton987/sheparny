""" Events permissions """
from rest_framework import permissions


class EventOwnerPermission(permissions.BasePermission):
    """
    Allows safe request and validates if the user is authenticated
    and owner of the event
    """
    def has_permission(self, request, view):
        """
        Returns true or false if the Account has the permission
        :param request: Request made by the Account
        :param view: View set
        :return: Boolean with the Account permission
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Returns `True` if the user is owner of the event
        :param request: Request made by the user
        :param view: View set
        :param obj: Event instance
        :return: Boolean with the Account permission
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
