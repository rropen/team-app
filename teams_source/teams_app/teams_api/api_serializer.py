from rest_framework import serializers
from teams_app.models import Relationship, Team, Role, UserProfile
from django.contrib.auth.models import User

#JC General Serializers which link to the models
#JC - Basic User Serializer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    role_info = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "role_info"]

    def get_role_info(self, obj):
        serializer = RoleSerializer(Relationship.objects.get(user=obj, status=1, team=self.root.instance[0]).role)
        return serializer.data

#JC - Basic Team Serializer
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"


#JC - Serializer for api/teams
class UsersTeamsSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    class Meta:
        model = Relationship
        fields = ["team", "role"]


#JC - Serializers for api/members
class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Relationship
        fields = ["user"]

class AdditionalTeam(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True)
    class Meta:
        model = Team
        fields = ["id", "name", "description", "private", "members"]