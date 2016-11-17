from .models import *
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project

class ConsultantSerializer(serializers.ModelSerializer):
    project_id=ProjectSerializer()
    class Meta:
        model = Consultant


