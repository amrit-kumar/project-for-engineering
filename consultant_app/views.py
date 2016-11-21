from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets

from .serializers import  *



class AdminPanelViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Consultant.objects.all()
    serializer_class = AdminPanelSerializer

class AdminPanelAddSupporter(viewsets.ModelViewSet):
    queryset = Supporter.objects.all()
    serializer_class = AdminPanelAddSupporterSerializer




