
from rest_framework import serializers
from .models import User, Team, Activity, Workout, Leaderboard
from bson import ObjectId

class TeamSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='pk', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name']

    def validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError("O nome deve ser uma string não vazia.")
        if len(value) > 100:
            raise serializers.ValidationError("O nome deve ter no máximo 100 caracteres.")
        return value

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='pk')
    team = serializers.SerializerMethodField(read_only=True)
    team_id = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'team_id']

    def get_team(self, obj):
        try:
            team = Team.objects.get(pk=ObjectId(obj.team_id))
            return TeamSerializer(team).data
        except Team.DoesNotExist:
            return None

    def validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError("O nome deve ser uma string não vazia.")
        if len(value) > 100:
            raise serializers.ValidationError("O nome deve ter no máximo 100 caracteres.")
        return value

    def validate_email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise serializers.ValidationError("E-mail inválido.")
        return value

    def validate_team_id(self, value):
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("ID de time inválido.")
        if not Team.objects.filter(pk=ObjectId(value)).exists():
            raise serializers.ValidationError("Time não encontrado.")
        return value

class ActivitySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='pk')
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_id', 'activity', 'duration']

    def validate_activity(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError("A atividade deve ser uma string não vazia.")
        return value

    def validate_duration(self, value):
        if not isinstance(value, int) or value <= 0:
            raise serializers.ValidationError("A duração deve ser um inteiro positivo.")
        return value

class WorkoutSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='pk')

    class Meta:
        model = Workout
        fields = ['id', 'name', 'suggested_for']

    def validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError("O nome do treino deve ser uma string não vazia.")
        return value

class LeaderboardSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True, source='pk')
    user = UserSerializer(read_only=True)
    user_id = serializers.CharField(write_only=True)

    class Meta:
        model = Leaderboard
        fields = ['id', 'user', 'user_id', 'points']

    def validate_points(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Os pontos devem ser um inteiro não negativo.")
        return value

    id = serializers.CharField(read_only=True, source='pk')
    team = serializers.SerializerMethodField(read_only=True)
    team_id = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'team', 'team_id']

    def get_team(self, obj):
        try:
            team = Team.objects.get(pk=ObjectId(obj.team_id))
            return TeamSerializer(team).data
        except Team.DoesNotExist:
            return None

    def validate_name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise serializers.ValidationError("O nome deve ser uma string não vazia.")
        if len(value) > 100:
            raise serializers.ValidationError("O nome deve ter no máximo 100 caracteres.")
        return value

    def validate_email(self, value):
        if not isinstance(value, str) or '@' not in value:
            raise serializers.ValidationError("E-mail inválido.")
        return value

    def validate_team_id(self, value):
        if not ObjectId.is_valid(value):
            raise serializers.ValidationError("ID de time inválido.")
        if not Team.objects.filter(pk=ObjectId(value)).exists():
            raise serializers.ValidationError("Time não encontrado.")
        return value
        model = Leaderboard
        fields = ['id', 'user', 'user_id', 'points']

    def validate_points(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("Os pontos devem ser um inteiro não negativo.")
        return value
