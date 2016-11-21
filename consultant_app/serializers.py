from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.serializers.json import Serializer as Builtin_Serializer

class USER_MODEL_SERIALIAZER(serializers.ModelSerializer):
    class Meta:
        model= UserProfile
        # exclude = ('',)

        # fields= ('username', )


# class TokenSerialiazer(serializers.ModelSerializer):
#     class Meta:
#         model=Token


class SupporterSerializer(serializers.ModelSerializer):
    supporter= USER_MODEL_SERIALIAZER()


    class Meta:
        model= Supporter
        fields=('pk','supporter', )
        ordering = ('-pk',)


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model= Project
        fields=( 'pk','title',)
        ordering = ('pk',)

class AdminPanelSerializer(serializers.ModelSerializer):
    supporter= SupporterSerializer()
    project= ProjectSerializer()
    consultant= USER_MODEL_SERIALIAZER()
    class Meta:
        model= Consultant
        depth= 1
        fields=('pk', 'consultant','project','supporter')
        ordering = ('pk',)

class AdminPanelAddSupporterSerializer(serializers.ModelSerializer):
    supporter= SupporterSerializer()
    class Meta:
        model= Supporter
        fields=('supporter', 'employee_id', 'skype_username','mobile_no')

