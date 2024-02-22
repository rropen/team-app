from rest_framework import serializers
from teams_app.models import Relationship, Team, Role, Status
from django.contrib.auth.models import User

#JC General Serializers which link to the models
#JC - Basic User Serializer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class UserSerializerAddon(serializers.ModelSerializer):
    role_info = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "role_info"]

    def get_role_info(self, obj):
        serializer = RoleSerializer(Relationship.objects.get(user=obj, status=1, team=self.root.instance[0]).role)
        return serializer.data

#JC - Basic Team Serializer
class TeamSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Team
        fields = ["name", "description", "notes", "count"]


#JC - Serializer for api/teams
class UsersTeamsSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    class Meta:
        model = Relationship
        fields = ["team", "role"]


#JC - Serializers for api/members
class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializerAddon(read_only=True)
    class Meta:
        model = Relationship
        fields = ["user"]

class AdditionalTeam(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    class Meta:
        model = Team
        fields = ["id", "name", "description", "private", "members"]


class TeamRelated(serializers.SlugRelatedField):
    def get_queryset(self):
        queryset = self.queryset
        if hasattr(self.root, 'name'):
            queryset = queryset.filter(name=self.name)


class RelationshipSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    team = serializers.SlugRelatedField(slug_field='name', queryset=Team.objects.all())
    role = serializers.SlugRelatedField(slug_field='role', queryset=Role.objects.all())
    status = serializers.SlugRelatedField(slug_field='status', queryset=Status.objects.all())

    class Meta:
        model = Relationship
        fields = "__all__"

    def create(self, validated_data):
        rel = Relationship(
            user = User.objects.get(username=validated_data['user']),
            team = Team.objects.get(name=validated_data["team"]),
            role = Role.objects.get(role=validated_data["role"]),
            status = Status.objects.get(status=validated_data["status"])
        )
        rel.save()
        return rel

class JoinableTeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = ['team']