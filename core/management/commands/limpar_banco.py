from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from core.models import (
    Voluntario,
    AcaoComunitaria,
    Inscricao,
    Campanha,
)


class Command(BaseCommand):
    help = 'Limpa o banco de dados mantendo apenas admins e superusuários'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Iniciando limpeza do banco...'))

        # 🔴 1. Deletar dependentes primeiro
        inscricoes = Inscricao.objects.all().count()
        Inscricao.objects.all().delete()
        self.stdout.write(f'Inscrições removidas: {inscricoes}')

        # 🔴 2. Deletar ações
        acoes = AcaoComunitaria.objects.all().count()
        AcaoComunitaria.objects.all().delete()
        self.stdout.write(f'Ações removidas: {acoes}')

        # 🔴 3. Deletar campanhas
        campanhas = Campanha.objects.all().count()
        Campanha.objects.all().delete()
        self.stdout.write(f'Campanhas removidas: {campanhas}')

        # 🔴 4. Deletar voluntários
        voluntarios = Voluntario.objects.all().count()
        Voluntario.objects.all().delete()
        self.stdout.write(f'Voluntários removidos: {voluntarios}')

        # 🔴 5. Deletar usuários NÃO admin
        usuarios = User.objects.filter(
            is_superuser=False,
            is_staff=False
        )

        total_usuarios = usuarios.count()
        usuarios.delete()

        self.stdout.write(f'Usuários comuns removidos: {total_usuarios}')

        self.stdout.write(self.style.SUCCESS('Banco limpo com sucesso!'))