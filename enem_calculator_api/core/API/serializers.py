from rest_framework import serializers

from enem_calculator_api.core.models import User, Ambition, Simulation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']


class AmbitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambition
        fields = ['id', 'name', 'description', 'score']


class SimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Simulation
        fields = ['id', 'user', 'ambition', 'score', 'date']
