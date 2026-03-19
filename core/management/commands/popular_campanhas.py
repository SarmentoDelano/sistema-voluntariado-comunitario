from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core.models import Campanha


class Command(BaseCommand):
    help = 'Popula o banco com campanhas de exemplo'

    def handle(self, *args, **kwargs):
        admin_user = User.objects.filter(is_staff=True).first()

        if not admin_user:
            admin_user = User.objects.create_user(
                username='admin_seed',
                email='admin_seed@email.com',
                password='123456',
                is_staff=True,
                is_superuser=False
            )
            self.stdout.write(self.style.WARNING(
                'Nenhum admin encontrado. Usuário admin_seed criado com senha 123456.'
            ))

        hoje = date.today()

        campanhas = [
            {
                'nome': 'Campanha do Agasalho Solidário',
                'descricao': 'Arrecadação de roupas e cobertores para famílias em situação de vulnerabilidade social durante o período de frio.',
                'data_inicio': hoje,
                'data_fim': hoje + timedelta(days=20),
                'local': 'Centro Comunitário de Brotas',
                'status': 'ativa',
            },
            {
                'nome': 'Campanha de Alimentos Não Perecíveis',
                'descricao': 'Mobilização para arrecadação de alimentos destinados à montagem de cestas básicas para famílias cadastradas na comunidade.',
                'data_inicio': hoje + timedelta(days=2),
                'data_fim': hoje + timedelta(days=25),
                'local': 'Igreja Batista do Bairro',
                'status': 'ativa',
            },
            {
                'nome': 'Campanha de Doação de Material Escolar',
                'descricao': 'Coleta de cadernos, lápis, mochilas e outros materiais escolares para apoiar crianças em idade escolar.',
                'data_inicio': hoje + timedelta(days=5),
                'data_fim': hoje + timedelta(days=30),
                'local': 'Escola Comunitária Esperança',
                'status': 'ativa',
            },
            {
                'nome': 'Campanha de Arrecadação de Produtos de Higiene',
                'descricao': 'Recebimento de sabonetes, escovas de dente, creme dental e outros itens de higiene pessoal para doação.',
                'data_inicio': hoje - timedelta(days=10),
                'data_fim': hoje + timedelta(days=10),
                'local': 'Associação de Moradores de Brotas',
                'status': 'ativa',
            },
            {
                'nome': 'Campanha de Apoio à Inclusão Digital',
                'descricao': 'Coleta de equipamentos usados, como computadores e periféricos, para recondicionamento e uso em projetos sociais.',
                'data_inicio': hoje - timedelta(days=30),
                'data_fim': hoje - timedelta(days=5),
                'local': 'Biblioteca Comunitária de Salvador',
                'status': 'encerrada',
            },
            {
                'nome': 'Campanha de Natal Solidário',
                'descricao': 'Organização de doações de brinquedos, roupas e alimentos para distribuição em ações de fim de ano.',
                'data_inicio': hoje + timedelta(days=15),
                'data_fim': hoje + timedelta(days=45),
                'local': 'Praça Central de Brotas',
                'status': 'ativa',
            },
        ]

        criadas = 0

        for campanha in campanhas:
            obj, created = Campanha.objects.get_or_create(
                nome=campanha['nome'],
                data_inicio=campanha['data_inicio'],
                defaults={
                    'descricao': campanha['descricao'],
                    'data_fim': campanha['data_fim'],
                    'local': campanha['local'],
                    'status': campanha['status'],
                    'criado_por': admin_user,
                }
            )

            if created:
                criadas += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Campanha criada: {obj.nome}'
                ))
            else:
                self.stdout.write(
                    f'Campanha já existia: {obj.nome}'
                )

        self.stdout.write(self.style.SUCCESS(
            f'Concluído! {criadas} nova(s) campanha(s) criada(s).'
        ))