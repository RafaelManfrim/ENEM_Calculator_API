from rest_framework import viewsets

from enem_calculator_api.core.API.serializers import UserSerializer, AmbitionSerializer, SimulationSerializer
from enem_calculator_api.core.models import User, Ambition, Simulation


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AmbitionViewset(viewsets.ModelViewSet):
    queryset = Ambition.objects.all()
    serializer_class = AmbitionSerializer


class SimulationViewset(viewsets.ModelViewSet):
    queryset = Simulation.objects.all()
    serializer_class = SimulationSerializer
