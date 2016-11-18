from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=Token


class SupporterSerializer(serializers.ModelSerializer):
    class Meta:
        model= Supporter
        fields=('user__username', 'pk')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project
        fields=('user__username', 'pk')


class AdminPanelSerializer(serializers.ModelSerializer):
    supporter_id= SupporterSerializer()
    project_id= ProjectSerializer()
    class Meta:
        model= Consultant
        fields=('pk', 'supporter_id', 'project_id', 'user_username')


class ConsultantSerializer(serializers.ModelSerializer):
    project_id=ProjectSerializer()
    class Meta:
        model = Consultant

