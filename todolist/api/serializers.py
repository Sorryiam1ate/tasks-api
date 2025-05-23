from rest_framework import serializers

from .models import AstanaHubParticipant, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstanaHubParticipant
        fields = '__all__'
