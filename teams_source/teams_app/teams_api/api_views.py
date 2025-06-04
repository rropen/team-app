from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from teams_app.models import Relationship, Team, Role, Status
from teams_app.teams_api.api_utils import verify_user_token, get_role_of_user_in_team, has_permitted_role
from .api_serializer import UsersTeamsSerializer, AdditionalTeam, TeamSerializer, RelationshipSerializer
from rest_framework.exceptions import NotFound, AuthenticationFailed, PermissionDenied
from django.db.models.functions import Lower
from rest_framework import permissions 
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect, JsonResponse
from django.http.request import HttpRequest
from .serializers.teams_list import AllTeamSerializer
from django.shortcuts import get_object_or_404
from rest_framework_api_key.permissions import HasAPIKey

class MembersTeamViewSet(viewsets.ModelViewSet):
    """
    API View that compiles a list of data about team members of a particular team.

    On the Absence Planner, this is needed for the edit team page and specific team calendar ("view team") page.

    This is accessible to any authenticated users.
    """

    serializer_class = AdditionalTeam
    permission_classes = [permissions.AllowAny, HasAPIKey]

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
    """
    Utility API View that reads all of the data about teams that a user is already in, as well as their team members.
    Permissions are validated with the username derived from the user token in the request header.

    In the Absence Planner, this is used for the:
        - Teams Dashboard (where the user can see teams they have already joined)
            - Authenticated Users
        - Absence Calendar (where the user can see the absences of all the teams they are in)
            - Authenticated Users
    """

    serializer_class = AllTeamSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        # We need a username from the user token so that we can only get the teams associated with that user.
        username = verify_user_token(self.request)

        sort = self.request.query_params.get("sort")

        # We do not need to check if a user with that username exists because
        # that is done in the verify_user_token utility function anyways.

        if sort is not None and sort != "None":
            return Relationship.objects.order_by(sort).filter(user__username=username, status_id=1).all()
        else:
            return Relationship.objects.order_by("-favourite").filter(user__username=username, status_id=1).all()

class TeamView(viewsets.ModelViewSet):
    """
    A general-purpose API View for CRUD operations on teams data. Permissions are validated
    with the username derived from the user token in the request header.

    CRUD operations as used in the Absence Planner include:
        - Creating a team (Create)
            - Authenticated Users
        - Viewing teams that the user is not already in (Read)
            - Authenticated Users
        - Editing a team (Update)
            - Team Owner
        - Deleting a team (Delete)
            - Team Owner
    """

    serializer_class = TeamSerializer
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        """
        View joinable teams
        """
        username = verify_user_token(self.request)
        try:
            User.objects.get(username=username)
        except:
            raise NotFound(detail="Error, invalid username", code=404)
        
        # Exclude teams the user is not already in
        exclude_list = Relationship.objects.filter(user__username=username, status_id=1).values_list('team_id')

        return Team.objects.filter(private=False).exclude(id__in=exclude_list)
    
    def create(self, request:HttpRequest):
        """
        Create, edit, or delete a team
        """
        method = request.query_params.get("method")
        username = verify_user_token(self.request)
        if ((str(method).lower() == "edit") or str(method).lower() == "delete"):
            team = Team.objects.get(id=request.data["id"])
            role = get_role_of_user_in_team(username, team.id)

        if method and str(method).lower() == "edit": # Edit a team
            has_permitted_role(role, ["Owner", "Co-Owner"])

            team.name = request.data["name"]
            team.description = request.data["description"]
            if request.data.get("private"):
                team.private = True
            else:
                team.private = False
            team.save()
            return JsonResponse(data={"message": "success"}, status=200)
        elif method and str(method).lower() == "delete": # Delete a team
            has_permitted_role(role, ["Owner", "Co-Owner"])

            team.delete()
            return JsonResponse(data={"message": "success"}, status=200)
        else: # Create Team
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

            # Add Team Owner
            # We do not need to check if a user with that username exists because
            # that is done in the verify_user_token utility function anyways.
            owner_data = {
                "user": User.objects.get(username=username),
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
    """
    API view that queries for teams the user is not already in.

    This is not used for anything in particular in Absence Planner.
    """

    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny, HasAPIKey]

    def get_queryset(self):
        username = self.request.query_params.get("username")
        if not username:
            raise NotFound(detail="Error, no given username", code=404)
        elif not User.objects.filter(username=username).exists():
            raise NotFound(detail="Error, invalid username", code=404)

        return Team.objects.all().exclude(relationship__user=User.objects.get(username=username))


class ManageTeam(viewsets.ModelViewSet):
    """
    API View used for allowing members to leave, join, and favourite teams.

    On the Absence Planner, these are used for various pages.

    Only authenticated users who "own" that data (e.g., a team member can only
    leave team for themselves) can use these methods. You cannot perform an action
    in another users name without validating the user token / username first.
    """

    serializer_class = RelationshipSerializer
    permission_classes = [HasAPIKey]

    def create(self, request:HttpRequest):
        username = verify_user_token(request)
        method = request.query_params.get("method")
        if not method:
            return JsonResponse(data={"error": "Invalid Method (Join, Leave)"}, status=404)

        team_id = request.data["team"]

        if str(method).lower() == "join":
            if not request.data.get("team"):
                return JsonResponse(data={"error": "Team ID not provided"}, status=404)
            team_data = {
                "user": User.objects.get(username=username),
                "team": Team.objects.get(id=team_id),
                "role": Role.objects.get(role="Member"),
                "status": Status.objects.get(status="Active")
            }

            serializer = RelationshipSerializer(data=team_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return JsonResponse(data={"message": "success"}, status=200)
        
        elif str(method).lower() == "leave":
            rel = Relationship.objects.filter(user__username=username, team__id=team_id, status=Status.objects.get(status="Active"))
            if not rel.exists():
                return JsonResponse(data={"error": "Relationship not found"} ,status=404)
            
            rel[0].delete()
            return JsonResponse(data={"message": "success"}, status=200)

        elif str(method).lower() == "favourite":
            rel = Relationship.objects.filter(user__username=username, team__id=team_id, status=Status.objects.get(status="Active"))
            if not rel.exists():
                return JsonResponse(data={"error": "Relationship not found"} ,status=404)
            
            teamRel:Relationship = rel[0]
            teamRel.favourite = not teamRel.favourite # Toggle the favourite value

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

    permission_classes = [permissions.AllowAny, HasAPIKey]

    def list(self, request):
        username = self.request.query_params.get("username")

        try:
            User.objects.get(username=username)
        except:
            return Response(False, status=200)
        
        return Response(True, status=200)