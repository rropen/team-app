from rest_framework import serializers
from teams_app.models import Relationship, Team
from django.contrib.auth.models import User

# Purpose - This API lists the teams of a given user
# URL - api/teams/?username=USERNAME

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]

class TeamMemberSerializerNormal(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Relationship
        fields = ["user"]

class TeamSerializerAddon(serializers.ModelSerializer):
    members = TeamMemberSerializerNormal(many=True)
    class Meta:
        model = Team
        fields = ["id", "name", "description", "private", "members"]

class AllTeamSerializer(serializers.ModelSerializer):
    team = TeamSerializerAddon(read_only=True)
    class Meta:
        model = Relationship
        fields = ["team"]