from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.permissions import IsOwnerOrAdmin
from core.permissions import IsAdminOrReadOnly
from core.permissions import IsOwner
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView
from .models import Voluntario, AcaoComunitaria, Inscricao, Campanha
from .serializers import (
    VoluntarioSerializer,
    AcaoComunitariaSerializer,
    InscricaoSerializer,
    CampanhaSerializer,
)
from django.shortcuts import render
from django.http import HttpResponse


class CustomLoginView(LoginView):
    template_name = 'login.html'

def cadastro_voluntario_view(request):
    return render(request, 'cadastro_voluntario.html')

def acoes_list(request):
    return HttpResponse("Página de ações")

def campanhas(request):
    return HttpResponse("Página de campanhas")

def minhas_inscricoes(request):
    return HttpResponse("Página de minhas inscrições")

class VoluntarioViewSet(viewsets.ModelViewSet):
    queryset = Voluntario.objects.all()
    serializer_class = VoluntarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def perform_update(self, serializer):
        user = serializer.instance.user

        # Verifica se estão tentando mudar is_staff
        new_is_staff = self.request.data.get('is_staff')

        if new_is_staff is not None:
            # Só o dono pode fazer isso
            if self.request.user.username != settings.OWNER_USERNAME:
                raise PermissionDenied("Apenas o dono do sistema pode alterar permissões de administrador.")

            user.is_staff = new_is_staff
            user.save()

        serializer.save()


class AcaoComunitariaViewSet(viewsets.ModelViewSet):
    queryset = AcaoComunitaria.objects.all().order_by('data', 'horario')
    serializer_class = AcaoComunitariaSerializer
    permission_classes = [IsAdminOrReadOnly]


class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(voluntario=self.request.user.voluntario)


class CampanhaViewSet(viewsets.ModelViewSet):
    queryset = Campanha.objects.all()
    serializer_class = CampanhaSerializer
    permission_classes = [IsAdminOrReadOnly]