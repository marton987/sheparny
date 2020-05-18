""" Accounts urls """
from django.urls import include, path, re_path
from rest_framework import routers

from accounts import views

ROUTER = routers.SimpleRouter(trailing_slash=False)
# Accounts Routes
ROUTER.register(r'accounts', views.AccountViewSet, 'accounts')

urlpatterns = [
    re_path(r'^auth/login$', views.LoginView.as_view(), name='login'),
    re_path(r'^auth/logout$', views.LogoutView.as_view(), name='logout'),
    path('', include(ROUTER.urls)),
]
