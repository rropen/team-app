from django.urls import include, path, re_path
from rest_framework import routers
from .api_views import *

router = routers.DefaultRouter()

router.register(r"teams", TeamViewSet, basename="teams")
router.register(r"users_teams", RelationshipViewSet, basename="users_teams")

urlpatterns = [
    path('', include(router.urls)),
    re_path('^users_teams/(?P<username>.+)/$', RelationshipViewSet),
]