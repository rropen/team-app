from .models import Team, Role, Relationship, Status, UserProfile
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import TeamSerializer, RelationshipSerializer
from urllib.parse import unquote
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics


class TeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = TeamSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Team.objects.all()
        return queryset
    
class RelationshipViewSet(viewsets.ModelViewSet):
    serializer_class = RelationshipSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")
        return Relationship.objects.filter(user__username=username).all()
