from .models import Team, Role, Relationship, Status, UserProfile
from rest_framework import serializers


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'notes', 'private']

class RelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Relationship
        fields = ['id', 'user_id', 'team_id', 'role_id', 'status_id']