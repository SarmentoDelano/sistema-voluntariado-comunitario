from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Voluntario(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='voluntario'
    )
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    disponibilidade = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class AcaoComunitaria(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('cancelada', 'Cancelada'),
        ('finalizada', 'Finalizada'),
    ]

    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    data = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativa')
    criado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='acoes_criadas'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Inscricao(models.Model):
    STATUS_PARTICIPACAO_CHOICES = [
        ('inscrito', 'Inscrito'),
        ('presente', 'Presente'),
        ('ausente', 'Ausente'),
    ]

    voluntario = models.ForeignKey(
        Voluntario,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )
    acao = models.ForeignKey(
        AcaoComunitaria,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )
    data_inscricao = models.DateTimeField(auto_now_add=True)
    status_participacao = models.CharField(
        max_length=20,
        choices=STATUS_PARTICIPACAO_CHOICES,
        default='inscrito'
    )

    class Meta:
        unique_together = ('voluntario', 'acao')
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    def __str__(self):
        return f'{self.voluntario} - {self.acao}'


class Campanha(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('encerrada', 'Encerrada'),
    ]

    nome = models.CharField(max_length=150)
    descricao = models.TextField()

    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True, help_text="Data limite da campanha")

    local = models.CharField(max_length=255, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativa'
    )

    criado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='campanhas_criadas'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome