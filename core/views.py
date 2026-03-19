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
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('acoes_list')



def cadastro_voluntario_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        disponibilidade = request.POST.get('disponibilidade')

        # validação simples
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username já existe.')
            return redirect('cadastro_voluntario')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # cria voluntário vinculado
        Voluntario.objects.create(
            user=user,
            telefone=telefone,
            endereco=endereco,
            disponibilidade=disponibilidade
        )

        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('login')

    return render(request, 'cadastro_voluntario.html')

def acoes_list(request):
    acoes = AcaoComunitaria.objects.all().order_by('data', 'horario')
    return render(request, 'acoes_list.html', {'acoes': acoes})

@login_required
@user_passes_test(lambda u: u.is_staff)
def campanhas(request):
    campanhas = Campanha.objects.all().order_by('nome')
    return render(request, 'campanhas.html', {'campanhas': campanhas})


@login_required
def minhas_inscricoes(request):
    inscricoes = Inscricao.objects.filter(
        voluntario=request.user.voluntario
    ).select_related('acao').order_by('acao__data', 'acao__horario')

    return render(request, 'minhas_inscricoes.html', {
        'inscricoes': inscricoes
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def acao_create(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        local = request.POST.get('local')
        status = request.POST.get('status')

        form_data = {
            'titulo': titulo,
            'descricao': descricao,
            'data': data,
            'horario': horario,
            'local': local,
            'status': status,
        }

        if not all([titulo, descricao, data, horario, local, status]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'acao_form.html', {
                'page_title': 'Nova Ação Comunitária',
                'form_data': form_data
            })

        AcaoComunitaria.objects.create(
            titulo=titulo,
            descricao=descricao,
            data=data,
            horario=horario,
            local=local,
            status=status,
            criado_por=request.user
        )

        messages.success(request, 'Ação comunitária criada com sucesso!')
        return redirect('acoes_list')

    return render(request, 'acao_form.html', {
        'page_title': 'Nova Ação Comunitária',
        'form_data': {}
    })

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


@login_required
def inscrever_acao(request, acao_id):
    if request.method != 'POST':
        return redirect('acoes_list')

    if request.user.is_staff:
        messages.error(request, 'Administradores não podem se inscrever em ações.')
        return redirect('acoes_list')

    try:
        voluntario = request.user.voluntario
    except Voluntario.DoesNotExist:
        messages.error(request, 'Seu usuário não possui perfil de voluntário.')
        return redirect('acoes_list')

    acao = get_object_or_404(AcaoComunitaria, id=acao_id)

    if acao.status != 'ativa':
        messages.error(request, 'Só é possível se inscrever em ações ativas.')
        return redirect('acoes_list')

    inscricao_existente = Inscricao.objects.filter(
        voluntario=voluntario,
        acao=acao
    ).exists()

    if inscricao_existente:
        messages.warning(request, 'Você já está inscrito nesta ação.')
        return redirect('acoes_list')

    Inscricao.objects.create(
        voluntario=voluntario,
        acao=acao,
        status_participacao='pendente'
    )

    messages.success(request, 'Inscrição realizada com sucesso!')
    return redirect('acoes_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def acao_update(request, acao_id):
    acao = get_object_or_404(AcaoComunitaria, id=acao_id)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        local = request.POST.get('local')
        status = request.POST.get('status')

        form_data = {
            'titulo': titulo,
            'descricao': descricao,
            'data': data,
            'horario': horario,
            'local': local,
            'status': status,
        }

        if not all([titulo, descricao, data, horario, local, status]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'acao_form.html', {
                'page_title': 'Editar Ação Comunitária',
                'form_data': form_data,
                'is_edit': True,
                'acao': acao,
            })

        acao.titulo = titulo
        acao.descricao = descricao
        acao.data = data
        acao.horario = horario
        acao.local = local
        acao.status = status
        acao.save()

        messages.success(request, 'Ação comunitária atualizada com sucesso!')
        return redirect('acoes_list')

    form_data = {
        'titulo': acao.titulo,
        'descricao': acao.descricao,
        'data': acao.data.strftime('%Y-%m-%d') if acao.data else '',
        'horario': acao.horario.strftime('%H:%M') if acao.horario else '',
        'local': acao.local,
        'status': acao.status,
    }

    return render(request, 'acao_form.html', {
        'page_title': 'Editar Ação Comunitária',
        'form_data': form_data,
        'is_edit': True,
        'acao': acao,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def inscritos_acao(request, acao_id):
    acao = get_object_or_404(AcaoComunitaria, id=acao_id)
    inscricoes = Inscricao.objects.filter(
        acao=acao
    ).select_related('voluntario__user', 'acao').order_by('voluntario__user__first_name', 'voluntario__user__username')

    return render(request, 'inscritos_acao.html', {
        'acao': acao,
        'inscricoes': inscricoes,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def marcar_presenca(request, inscricao_id):
    if request.method != 'POST':
        return redirect('acoes_list')

    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    inscricao.status_participacao = 'presente'
    inscricao.save()

    messages.success(request, 'Presença marcada com sucesso.')
    return redirect('inscritos_acao', acao_id=inscricao.acao.id)


@login_required
@user_passes_test(lambda u: u.is_staff)
def marcar_ausencia(request, inscricao_id):
    if request.method != 'POST':
        return redirect('acoes_list')

    inscricao = get_object_or_404(Inscricao, id=inscricao_id)
    inscricao.status_participacao = 'ausente'
    inscricao.save()

    messages.success(request, 'Ausência marcada com sucesso.')
    return redirect('inscritos_acao', acao_id=inscricao.acao.id)

@login_required
@user_passes_test(lambda u: u.is_staff)
def cancelar_acao(request, acao_id):
    if request.method != 'POST':
        return redirect('acoes_list')

    acao = get_object_or_404(AcaoComunitaria, id=acao_id)

    if acao.status == 'cancelada':
        messages.warning(request, 'Essa ação já está cancelada.')
        return redirect('acoes_list')

    acao.status = 'cancelada'
    acao.save()

    messages.success(request, 'Ação cancelada com sucesso.')
    return redirect('acoes_list')

@login_required
@user_passes_test(lambda u: u.is_staff)
def campanha_create(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        tipo_campanha = request.POST.get('tipo_campanha')

        form_data = {
            'nome': nome,
            'descricao': descricao,
            'tipo_campanha': tipo_campanha,
        }

        if not all([nome, descricao, tipo_campanha]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'campanha_form.html', {
                'page_title': 'Nova Campanha',
                'form_data': form_data,
                'is_edit': False,
            })

        Campanha.objects.create(
            nome=nome,
            descricao=descricao,
            tipo_campanha=tipo_campanha,
            criado_por=request.user
        )

        messages.success(request, 'Campanha criada com sucesso!')
        return redirect('campanhas')

    return render(request, 'campanha_form.html', {
        'page_title': 'Nova Campanha',
        'form_data': {},
        'is_edit': False,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def campanha_update(request, campanha_id):
    campanha = get_object_or_404(Campanha, id=campanha_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        tipo_campanha = request.POST.get('tipo_campanha')

        form_data = {
            'nome': nome,
            'descricao': descricao,
            'tipo_campanha': tipo_campanha,
        }

        if not all([nome, descricao, tipo_campanha]):
            messages.error(request, 'Preencha todos os campos obrigatórios.')
            return render(request, 'campanha_form.html', {
                'page_title': 'Editar Campanha',
                'form_data': form_data,
                'is_edit': True,
                'campanha': campanha,
            })

        campanha.nome = nome
        campanha.descricao = descricao
        campanha.tipo_campanha = tipo_campanha
        campanha.save()

        messages.success(request, 'Campanha atualizada com sucesso!')
        return redirect('campanhas')

    form_data = {
        'nome': campanha.nome,
        'descricao': campanha.descricao,
        'tipo_campanha': campanha.tipo_campanha,
    }

    return render(request, 'campanha_form.html', {
        'page_title': 'Editar Campanha',
        'form_data': form_data,
        'is_edit': True,
        'campanha': campanha,
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def campanha_delete(request, campanha_id):
    if request.method != 'POST':
        return redirect('campanhas')

    campanha = get_object_or_404(Campanha, id=campanha_id)
    campanha.delete()

    messages.success(request, 'Campanha excluída com sucesso!')
    return redirect('campanhas')