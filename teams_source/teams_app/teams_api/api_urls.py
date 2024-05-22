from django.urls import include, path, re_path
from rest_framework import routers
from teams_app.teams_api.api_views import *

router = routers.DefaultRouter()

#JC - Register api links
#router.register(r'teams', UserTeamViewSet, basename="teams")
router.register(r'members', MembersTeamViewSet, basename="members")
router.register(r'user/teams', AllUserTeamsViewSet, basename="users_teams")
router.register(r'teams', TeamView, basename="creator")
router.register(r'joinable', JoinableTeams, basename="joinable")
router.register(r'manage', ManageTeam, basename="manage")

urlpatterns = [
    path('', include(router.urls)),
    re_path('^members/(?P<team>.+)/$', MembersTeamViewSet),
    re_path('^members/(?P<id>.+)/$', MembersTeamViewSet),
    re_path('^teams/?P<username>.+/$', AllUserTeamsViewSet),
]