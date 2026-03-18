from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Voluntario


class Command(BaseCommand):
    help = 'Popula o banco com voluntários para testes'

    def handle(self, *args, **kwargs):
        voluntarios = [
            {
                "username": "joao123",
                "first_name": "João",
                "last_name": "Silva",
                "email": "joao@email.com",
                "password": "123456",
                "telefone": "(71) 99999-1111",
                "endereco": "Brotas, Salvador - BA",
                "disponibilidade": "Fins de semana",
            },
            {
                "username": "maria123",
                "first_name": "Maria",
                "last_name": "Souza",
                "email": "maria@email.com",
                "password": "123456",
                "telefone": "(71) 99999-2222",
                "endereco": "Pituba, Salvador - BA",
                "disponibilidade": "Noites",
            },
            {
                "username": "pedro123",
                "first_name": "Pedro",
                "last_name": "Oliveira",
                "email": "pedro@email.com",
                "password": "123456",
                "telefone": "(71) 99999-3333",
                "endereco": "Cabula, Salvador - BA",
                "disponibilidade": "Manhãs",
            },
        ]

        for item in voluntarios:
            user, created = User.objects.get_or_create(
                username=item["username"],
                defaults={
                    "first_name": item["first_name"],
                    "last_name": item["last_name"],
                    "email": item["email"],
                }
            )

            if created:
                user.set_password(item["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(
                    f'Usuário criado: {user.username}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Usuário já existe: {user.username}'
                ))

            voluntario, vol_created = Voluntario.objects.get_or_create(
                user=user,
                defaults={
                    "telefone": item["telefone"],
                    "endereco": item["endereco"],
                    "disponibilidade": item["disponibilidade"],
                }
            )

            if vol_created:
                self.stdout.write(self.style.SUCCESS(
                    f'Voluntário criado: {user.username}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Voluntário já existe: {user.username}'
                ))

        self.stdout.write(self.style.SUCCESS('População concluída com sucesso.'))