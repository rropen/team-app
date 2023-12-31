from django.urls import include, path, re_path
from rest_framework import routers
from teams_app.teams_api.api_views import *

router = routers.DefaultRouter()

#JC - Register api links
#router.register(r'teams', UserTeamViewSet, basename="teams")
router.register(r'members', MembersTeamViewSet, basename="members")
router.register(r'teams', AllUserTeamsViewSet, basename="users_teams")

urlpatterns = [
    path('', include(router.urls)),
    #re_path('^teams/(?P<username>.+)/$', UserTeamViewSet),
    re_path('^members/(?P<team>.+)/$', MembersTeamViewSet),
    re_path('^teams/?P<username>.+/$', AllUserTeamsViewSet)
]