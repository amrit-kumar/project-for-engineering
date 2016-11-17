from django.shortcuts import render
from .models import *
from rest_framework import viewsets
from .serializers import *

# Create your views here.

class ConsultantViewset(viewsets.ModelViewSet):
    queryset = Consultant.objects.filter(supporter_id=2)
    print(queryset)
    serializer_class = ConsultantSerializer
    # retrieve_serializer_class=ProjectSerializer




