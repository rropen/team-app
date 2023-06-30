from rest_framework import routers
from .api_views import *

api_router = routers.DefaultRouter()

api_router.register(r"teams", TeamViewSet, basename="teams")
api_router.register(r"users_teams", RelationshipViewSet, basename="users_teams")