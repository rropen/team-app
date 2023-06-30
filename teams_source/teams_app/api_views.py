from .models import Team, Role, Relationship, Status, UserProfile
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import TeamSerializer, RelationshipSerializer
from urllib.parse import unquote
from rest_framework.response import Response
from django.http import JsonResponse


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
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = RelationshipSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.kwargs["username"]
        return Relationship.objects.filter(team__username=username).values()
    
    """def list(self, request):
        user_name = unquote(request.GET['user_name'])

        results = Relationship.objects.filter(self.request.user).all()

        print(results)

        return JsonResponse({"results": list(results)})"""
    
class MemberViewSet(viewsets.ModelViewSet):

    serializer_class = TeamSerializer

    def list(self, request):

        search_string = unquote(request.GET['search_string'])

        results = Relationship.objects.filter(team__name=search_string)

        return Response(results)

    def get_queryset(self):
        queryset = Relationship.objects.none()
