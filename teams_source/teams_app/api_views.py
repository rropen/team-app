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
        return Relationship.objects.none()
    
    def list(self, request):
        username = request.query_params.get("username")
        teams = {}
        for i in Relationship.objects.filter(user__username=username).all():
            teams[i.team.id] = {
                "name": i.team.name,
                "description": i.team.description
            }
        return JsonResponse({"results": teams})