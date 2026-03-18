from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Voluntario, AcaoComunitaria, Inscricao, Campanha


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class VoluntarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Voluntario
        fields = ['id', 'user', 'telefone', 'endereco', 'disponibilidade']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', ''),
            password=user_data['password']
        )
        voluntario = Voluntario.objects.create(user=user, **validated_data)
        return voluntario


class AcaoComunitariaSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.username', read_only=True)

    class Meta:
        model = AcaoComunitaria
        fields = [
            'id',
            'titulo',
            'descricao',
            'data',
            'horario',
            'local',
            'status',
            'criado_por',
            'criado_por_nome',
            'created_at',
        ]
        read_only_fields = ['created_at']


class InscricaoSerializer(serializers.ModelSerializer):
    voluntario_nome = serializers.CharField(source='voluntario.user.username', read_only=True)
    acao_titulo = serializers.CharField(source='acao.titulo', read_only=True)

    class Meta:
        model = Inscricao
        fields = [
            'id',
            'voluntario',
            'voluntario_nome',
            'acao',
            'acao_titulo',
            'data_inscricao',
            'status_participacao',
        ]
        read_only_fields = ['data_inscricao']


class CampanhaSerializer(serializers.ModelSerializer):
    criado_por_nome = serializers.CharField(source='criado_por.username', read_only=True)

    class Meta:
        model = Campanha
        fields = [
            'id',
            'nome',
            'descricao',
            'tipo_campanha',
            'criado_por',
            'criado_por_nome',
            'created_at',
        ]
        read_only_fields = ['created_at']