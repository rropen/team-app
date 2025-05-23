from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from teams_app.models import Relationship, Team, Role, Status
from .api_serializer import UsersTeamsSerializer, AdditionalTeam, TeamSerializer, RelationshipSerializer
from rest_framework.exceptions import NotFound, AuthenticationFailed, PermissionDenied
from django.db.models.functions import Lower
from rest_framework import permissions 
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, JsonResponse
from django.http.request import HttpRequest
from .serializers.teams_list import AllTeamSerializer
from django.shortcuts import get_object_or_404
import hashlib
from rest_framework.views import APIView

def teams_permission_check(request:HttpRequest, username):
    token = request.META.get("HTTP_TEAMS_TOKEN")
    if not token:
        raise AuthenticationFailed("No Token Found")
    expected_token = hashlib.sha256((username + "AbsencePlanner").encode()).hexdigest()
    if expected_token != token:
        raise PermissionDenied("Invalid Token")

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
        id = self.request.query_params.get("id")
        
        if not team and not id:
            raise NotFound(detail="Error, no given team", code=404)
        
        if self.request.query_params.get("team"):
            if not Team.objects.get(name=team):
                raise NotFound(detail="Error, invalid team", code=404)
            return Team.objects.filter(name=team).all()
        elif self.request.query_params.get("id"):
            if not Team.objects.get(id=id):
                raise NotFound(detail="Error, invalid team", code=404)
            return Team.objects.filter(id=id).all()

        

class AllUserTeamsViewSet(viewsets.ModelViewSet):

    serializer_class = AllTeamSerializer

    def get_queryset(self):
        username = self.request.query_params.get("username")
        sort = self.request.query_params.get("sort")
        if not username:
            raise NotFound(detail={"error_msg": "Error, no given username", "code": "N"}, code=404)
        elif not User.objects.filter(username=username).exists():
            raise NotFound(detail={"error_msg": "Error, invalid username", "code": "I"}, code=404)


        teams_permission_check(self.request, username)

        if sort is not None and sort != "None":
            return Relationship.objects.order_by(sort).filter(user__username=username, status_id=1).all()
        else:
            return Relationship.objects.order_by("-favourite").filter(user__username=username, status_id=1).all()

class TeamView(viewsets.ModelViewSet):

    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.request.query_params.get("username")
        if not username:
            raise NotFound(detail="Error, no given username", code=404)
        elif not User.objects.filter(username=username).exists():
            raise NotFound(detail="Error, invalid username", code=404)
        
        exclude_list = Relationship.objects.filter(user__username=username, status_id=1).values_list('team_id')

        return Team.objects.filter(private=False).exclude(id__in=exclude_list)
    
    def create(self, request:HttpRequest):
        method = request.query_params.get("method")
        if method and str(method).lower() == "edit":
            team = Team.objects.get(id=request.data["id"])
            team.name = request.data["name"]
            team.description = request.data["description"]
            if request.data.get("private"):
                team.private = True
            else:
                team.private = False
            team.save()
            return JsonResponse(data={"message": "success"}, status=200)
        elif method and str(method).lower() == "delete":
            team = Team.objects.get(id=request.data["id"])
            team.delete()
            return JsonResponse(data={"message": "success"}, status=200)
        else:
            #Create Team
            team_data = request.data.dict()
            if team_data.get("private") is not None:
                if team_data["private"] == "on":
                    team_data["private"] = True
                else:
                    team_data["private"] = False
            else:
                team_data["private"] = False
            
            serializer = TeamSerializer(data=team_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            #Add Team Owner
            #Check if username exists
            if not User.objects.filter(username=request.data["username"]).exists():
                raise NotFound(detail="Error, invalid username", code=404)
            
            owner_data = {
                "user": User.objects.get(username=request.data["username"]),
                "team": Team.objects.get(name=serializer.data["name"]),
                "role": Role.objects.get(role="Owner"),
                "status": Status.objects.get(status="Active")
            }
            
            owner_serializer = RelationshipSerializer(data = owner_data)
            owner_serializer.is_valid()
            owner_serializer.save()

            team_id = Team.objects.get(name=serializer.data["name"]).id
            return JsonResponse(data={"message": "success", "id": team_id}, status=200)
        
        return JsonResponse(data={"error": "Invalid method"}, status=404)

class JoinableTeams(viewsets.ModelViewSet):

    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        username = self.request.query_params.get("username")
        if not username:
            raise NotFound(detail="Error, no given username", code=404)
        elif not User.objects.filter(username=username).exists():
            raise NotFound(detail="Error, invalid username", code=404)

        return Team.objects.all().exclude(relationship__user=User.objects.get(username=username))


class ManageTeam(viewsets.ModelViewSet):

    serializer_class = RelationshipSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request:HttpRequest):
        method = request.query_params.get("method")
        if not method:
            return JsonResponse(data={"error": "Invalid Method (Join, Leave)"}, status=404)

        if str(method).lower() == "join":
            if not request.data.get("username") or not request.data.get("team"):
                return JsonResponse(data={"error": "Username or Team ID not provided"}, status=404)
            team_data = {
                "user": User.objects.get(username=request.data["username"]),
                "team": Team.objects.get(id=request.data["team"]),
                "role": Role.objects.get(role="Member"),
                "status": Status.objects.get(status="Active")
            }

            serializer = RelationshipSerializer(data=team_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return JsonResponse(data={"message": "success"}, status=200)
        
        elif str(method).lower() == "leave":
            rel = Relationship.objects.filter(user__username=request.data["username"], team__id=request.data["team"], status=Status.objects.get(status="Active"))
            if not rel.exists():
                return JsonResponse(data={"error": "Relationship not found"} ,status=404)
            
            rel[0].delete()
            return JsonResponse(data={"message": "success"}, status=200)

        elif str(method).lower() == "favourite":
            print(request.data)
            rel = Relationship.objects.filter(user__username=request.data["username"], team__id=request.data["team"], status=Status.objects.get(status="Active"))
            if not rel.exists():
                return JsonResponse(data={"error": "Relationship not found"} ,status=404)
            
            teamRel:Relationship = rel[0]
            if teamRel.favourite:
                teamRel.favourite = False
            else:
                teamRel.favourite = True

            teamRel.save(force_update=True)
            return JsonResponse(data={"message": "success"}, status=200)

        else:
            return JsonResponse(data={"error": "Invalid Method"}, status=404)

class StatusCheck(viewsets.ViewSet):
    """
    Returns a success message, used to check if the Team App and API are running correctly.
    In the Absence Planner, this is used to show the user a 503 if the API is not running.
    """

    permission_classes = [permissions.AllowAny]

    def list(self, request):
        return Response("success", status=200)

class CheckUserExists(viewsets.ViewSet):
    """
    Checks if the user exists in the Team App database.
    In the Absence Planner, this is used to show the user validation error when registering their
    account so that they first create an account on the Team App.
    """

    permission_classes = [permissions.AllowAny]

    def list(self, request):
        username = self.request.query_params.get("username")
        print(username)
        try:
            teams_permission_check(self.request, username)
        except:
            return Response(status=403)

        try:
            User.objects.get(username=username)
        except:
            return Response(False, status=200)
        
        return Response(True, status=200)