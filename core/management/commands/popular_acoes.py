from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import AcaoComunitaria
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Popula o banco com ações comunitárias de exemplo'

    def handle(self, *args, **kwargs):
        # tenta pegar um admin existente
        admin_user = User.objects.filter(is_staff=True).first()

        # se não existir admin, cria um
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

        acoes = [
            {
                'titulo': 'Oficina de Inclusão Digital para Idosos',
                'descricao': 'Ação voltada ao ensino básico de uso de celular, WhatsApp e navegação na internet para idosos da comunidade.',
                'data': hoje + timedelta(days=3),
                'horario': time(9, 0),
                'local': 'Centro Comunitário de Brotas',
                'status': 'ativa',
            },
            {
                'titulo': 'Mutirão de Cadastro de Voluntários',
                'descricao': 'Evento para cadastramento de novos voluntários e apresentação das ações sociais disponíveis no bairro.',
                'data': hoje + timedelta(days=5),
                'horario': time(14, 30),
                'local': 'Associação de Moradores de Brotas',
                'status': 'ativa',
            },
            {
                'titulo': 'Aula de Informática Básica para Jovens',
                'descricao': 'Capacitação introdutória sobre digitação, uso de editores de texto e pesquisas acadêmicas na internet.',
                'data': hoje + timedelta(days=7),
                'horario': time(10, 0),
                'local': 'Escola Comunitária Esperança',
                'status': 'ativa',
            },
            {
                'titulo': 'Campanha de Arrecadação de Alimentos',
                'descricao': 'Mobilização para arrecadação e organização de cestas básicas destinadas a famílias em situação de vulnerabilidade.',
                'data': hoje + timedelta(days=10),
                'horario': time(8, 0),
                'local': 'Igreja Batista do Bairro',
                'status': 'ativa',
            },
            {
                'titulo': 'Treinamento de Segurança Digital',
                'descricao': 'Encontro educativo sobre golpes online, senhas seguras e boas práticas de proteção de dados pessoais.',
                'data': hoje + timedelta(days=12),
                'horario': time(15, 0),
                'local': 'Biblioteca Comunitária de Salvador',
                'status': 'ativa',
            },
            {
                'titulo': 'Reforço Escolar com Apoio Tecnológico',
                'descricao': 'Ação de apoio estudantil com uso de computadores e recursos digitais para alunos da rede pública.',
                'data': hoje + timedelta(days=15),
                'horario': time(13, 30),
                'local': 'Escola Municipal de Brotas',
                'status': 'ativa',
            },
            {
                'titulo': 'Feira de Serviços Comunitários',
                'descricao': 'Evento com divulgação de projetos sociais, cadastro em ações e orientações sobre acesso a serviços digitais.',
                'data': hoje + timedelta(days=18),
                'horario': time(9, 30),
                'local': 'Praça Central de Brotas',
                'status': 'ativa',
            },
            {
                'titulo': 'Ação de Suporte Tecnológico para Pequenos Negócios',
                'descricao': 'Atendimento comunitário para auxiliar pequenos empreendedores no uso de redes sociais e ferramentas digitais.',
                'data': hoje + timedelta(days=20),
                'horario': time(16, 0),
                'local': 'Sala de Apoio ao Empreendedor',
                'status': 'ativa',
            },
        ]

        criadas = 0

        for acao in acoes:
            obj, created = AcaoComunitaria.objects.get_or_create(
                titulo=acao['titulo'],
                data=acao['data'],
                defaults={
                    'descricao': acao['descricao'],
                    'horario': acao['horario'],
                    'local': acao['local'],
                    'status': acao['status'],
                    'criado_por': admin_user,
                }
            )

            if created:
                criadas += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Ação criada: {obj.titulo}'
                ))
            else:
                self.stdout.write(
                    f'Ação já existia: {obj.titulo}'
                )

        self.stdout.write(self.style.SUCCESS(
            f'Concluído! {criadas} nova(s) ação(ões) criada(s).'
        ))