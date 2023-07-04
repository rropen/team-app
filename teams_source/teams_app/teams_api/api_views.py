from rest_framework import viewsets
from teams_app.models import Relationship, Team
from .api_serializer import UsersTeamsSerializer, AdditionalTeam
from rest_framework.exceptions import NotFound
from django.contrib.auth.models import User

class UserTeamViewSet(viewsets.ModelViewSet):

    serializer_class = UsersTeamsSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")
        if not username:
            raise NotFound(detail="Error, no given username", code=404)
        elif not User.objects.filter(username=username).exists():
            raise NotFound(detail="Error, invalid username", code=404)
        return Relationship.objects.filter(user__username=username, status_id=1).all()

class MembersTeamViewSet(viewsets.ModelViewSet):

    serializer_class = AdditionalTeam

    def get_queryset(self):
        team = self.request.query_params.get("team")
        return Team.objects.filter(name=team).all()