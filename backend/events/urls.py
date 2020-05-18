""" Events urls """
from django.urls import include, path
from rest_framework import routers

from events import views

ROUTER = routers.SimpleRouter(trailing_slash=False)
# Accounts Routes
ROUTER.register(r'events', views.EventViewSet, 'events')

urlpatterns = [
    path('', include(ROUTER.urls)),
]
