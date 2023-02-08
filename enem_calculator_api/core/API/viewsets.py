from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from enem_calculator_api.core.API.serializers import UserSerializer, AmbitionSerializer, SimulationSerializer
from enem_calculator_api.core.models import User, Ambition, Simulation


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not name or not email or not password:
            return Response({'error': 'Alguma informação está faltando'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({'error': 'Sua senha deve ter no mínimo 6 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Já existe um usuário com esse e-mail.'}, status=status.HTTP_400_BAD_REQUEST)

        created_user = User.objects.create_user(name=name, email=email, password=password)

        serializer = self.serializer_class(created_user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class AmbitionViewset(viewsets.ModelViewSet):
    serializer_class = AmbitionSerializer

    def get_queryset(self):
        user = self.request.user
        return Ambition.objects.filter(user_id=user.id)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_available_ambitions(self, request):
        ambitions = self.get_queryset()

        available_ambitions = [{
            'value': ambition['id'],
            'label': f'{ambition["course"]} - {ambition["college"]} {ambition["city"]}'
        } for ambition in ambitions.values()]

        return Response(available_ambitions, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        ambitions = self.get_queryset()
        serializer = self.serializer_class(ambitions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        user = request.user
        city = request.data.get('city')
        college = request.data.get('college')
        course = request.data.get('course')
        math_weight = request.data.get('math_weight')
        languages_weight = request.data.get('languages_weight')
        human_science_weight = request.data.get('human_science_weight')
        science_weight = request.data.get('science_weight')
        essay_weight = request.data.get('essay_weight')

        if not city or not college or not course or not math_weight or not languages_weight or not human_science_weight or not science_weight or not essay_weight:
            return Response({'error': 'Alguma informação está faltando'}, status=status.HTTP_400_BAD_REQUEST)

        new_ambition = {
            'user': user,
            'city': city,
            'college': college,
            'course': course,
            'math_weight': math_weight,
            'languages_weight': languages_weight,
            'human_science_weight': human_science_weight,
            'science_weight': science_weight,
            'essay_weight': essay_weight
        }

        created_ambition = Ambition.objects.create(**new_ambition)

        serializer = self.serializer_class(created_ambition)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        ambition_id = kwargs.get('pk')

        if not ambition_id:
            return Response({'error': 'ID não informado'}, status=status.HTTP_400_BAD_REQUEST)

        city = request.data.get('city')
        college = request.data.get('college')
        course = request.data.get('course')
        math_weight = request.data.get('math_weight')
        languages_weight = request.data.get('languages_weight')
        human_science_weight = request.data.get('human_science_weight')
        science_weight = request.data.get('science_weight')
        essay_weight = request.data.get('essay_weight')

        if not city or not college or not course or not math_weight or not languages_weight or not human_science_weight or not science_weight or not essay_weight:
            return Response({'error': 'Alguma informação está faltando'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ambition = Ambition.objects.get(id=ambition_id)
            ambition.city = city
            ambition.college = college
            ambition.course = course
            ambition.math_weight = math_weight
            ambition.languages_weight = languages_weight
            ambition.human_science_weight = human_science_weight
            ambition.science_weight = science_weight
            ambition.essay_weight = essay_weight
            ambition.save()

            serializer = self.serializer_class(ambition)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ambition.DoesNotExist:
            return Response({'error': 'A meta buscada não existe'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        ambition_id = kwargs.get('pk')

        if not ambition_id:
            return Response({'error': 'ID não informado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ambition = Ambition.objects.get(id=ambition_id)
            ambition.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ambition.DoesNotExist:
            return Response({'error': 'A meta buscada não existe'}, status=status.HTTP_404_NOT_FOUND)


class SimulationViewset(viewsets.ModelViewSet):
    serializer_class = SimulationSerializer

    def get_queryset(self):
        user = self.request.user
        return Simulation.objects.filter(user_id=user.id)

    def list(self, request, *args, **kwargs):
        simulations = self.get_queryset()
        serializer = self.serializer_class(simulations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request, *args, **kwargs):
        user = request.user
        math_score = request.data.get('math_score')
        languages_score = request.data.get('languages_score')
        human_science_score = request.data.get('human_science_score')
        science_score = request.data.get('science_score')
        essay_score = request.data.get('essay_score')
        is_official = request.data.get('is_official')
        name = request.data.get('name')

        if not math_score or not name or not languages_score or not human_science_score or not science_score or not essay_score or not is_official:
            return Response({'error': 'Alguma informação está faltando'}, status=status.HTTP_400_BAD_REQUEST)

        ambitions = Ambition.objects.filter(user_id=user.id)

        if not ambitions:
            return Response({'error': 'Nenhuma meta cadastrada'}, status=status.HTTP_400_BAD_REQUEST)

        simulations = []

        for ambition in ambitions.values():
            math_weight = ambition['math_weight']
            languages_weight = ambition['languages_weight']
            human_science_weight = ambition['human_science_weight']
            science_weight = ambition['science_weight']
            essay_weight = ambition['essay_weight']
            city = ambition['city']
            college = ambition['college']
            course = ambition['course']

            math_score_with_weight = math_score * math_weight
            languages_score_with_weight = languages_score * languages_weight
            human_science_score_with_weight = human_science_score * human_science_weight
            science_score_with_weight = science_score * science_weight
            essay_score_with_weight = essay_score * essay_weight

            final_score = (math_score_with_weight + languages_score_with_weight + human_science_score_with_weight + science_score_with_weight + essay_score_with_weight) / (math_weight + languages_weight + human_science_weight + science_weight + essay_weight)

            new_simulation = {
                'user': user,
                'math': math_score,
                'languages': languages_score,
                'human_science': human_science_score,
                'science': science_score,
                'essay': essay_score,
                'is_official': is_official,
                'name': f'{name} - {course} - {college} {city}',
                'final_score': final_score,
                'ambition': Ambition.objects.get(id=ambition['id']),
            }

            created_simulation = Simulation.objects.create(**new_simulation)

            serializer = self.serializer_class(created_simulation)

            simulations.append(serializer.data)

        return Response(simulations, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        simulation_id = kwargs.get('pk')

        if not simulation_id:
            return Response({'error': 'ID não informado'}, status=status.HTTP_400_BAD_REQUEST)

        math_score = request.data.get('math_score')
        languages_score = request.data.get('languages_score')
        human_science_score = request.data.get('human_science_score')
        science_score = request.data.get('science_score')
        essay_score = request.data.get('essay_score')
        is_official = request.data.get('is_official')
        name = request.data.get('name')

        if not math_score or not name or not languages_score or not human_science_score or not science_score or not essay_score or not is_official:
            return Response({'error': 'Alguma informação está faltando'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            simulation = Simulation.objects.get(id=simulation_id)
            ambition = Ambition.objects.get(id=simulation.ambition_id)

            math_weight = ambition.math_weight
            languages_weight = ambition.languages_weight
            human_science_weight = ambition.human_science_weight
            science_weight = ambition.science_weight
            essay_weight = ambition.essay_weight

            math_score_with_weight = math_score * math_weight
            languages_score_with_weight = languages_score * languages_weight
            human_science_score_with_weight = human_science_score * human_science_weight
            science_score_with_weight = science_score * science_weight
            essay_score_with_weight = essay_score * essay_weight

            final_score = (math_score_with_weight + languages_score_with_weight + human_science_score_with_weight + science_score_with_weight + essay_score_with_weight) / (math_weight + languages_weight + human_science_weight + science_weight + essay_weight)

            simulation.math = math_score
            simulation.languages = languages_score
            simulation.human_science = human_science_score
            simulation.science = science_score
            simulation.essay = essay_score
            simulation.is_official = is_official
            simulation.name = name
            simulation.final_score = final_score
            simulation.save()

            serializer = self.serializer_class(simulation)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Simulation.DoesNotExist:
            return Response({'error': 'A simulação informada não existe'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        simulation_id = kwargs.get('pk')

        if not simulation_id:
            return Response({'error': 'ID não informado'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            simulation = Simulation.objects.get(id=simulation_id)
            simulation.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Simulation.DoesNotExist:
            return Response({'error': 'A simulação informada não existe'}, status=status.HTTP_404_NOT_FOUND)
