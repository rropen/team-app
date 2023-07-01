from rest_framework import serializers
from teams_app.models import Relationship, Team, Role
from django.contrib.auth.models import User

#JC - Basic User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]

#JC - Basic Team Serializer
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UsersTeamsSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    class Meta:
        model = Relationship
        fields = ["team", "role"]