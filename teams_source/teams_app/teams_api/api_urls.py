from django.urls import include, path, re_path
from rest_framework import routers
from teams_app.teams_api import api_views

router = routers.DefaultRouter()

#JC - Register api links
router.register(r'members',api_views.MembersTeamViewSet, basename="members")
router.register(r'user/teams', api_views.AllUserTeamsViewSet, basename="users_teams")
router.register(r'teams', api_views.TeamView, basename="creator")
router.register(r'joinable', api_views.JoinableTeams, basename="joinable")
router.register(r'manage', api_views.ManageTeam, basename="manage")
router.register(r'status_check', api_views.StatusCheck, basename="manage")
router.register(r'user_exists', api_views.CheckUserExists, basename="user_exists")

urlpatterns = [
    path('', include(router.urls)),
    re_path('^members/(?P<team>.+)/$', api_views.MembersTeamViewSet),
    re_path('^members/(?P<id>.+)/$', api_views.MembersTeamViewSet),
    re_path('^teams/?P<username>.+/$', api_views.AllUserTeamsViewSet),
]