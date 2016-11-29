from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import  *
from rest_framework.decorators import detail_route, list_route


class AdminPanelViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    queryset = User.objects.all().order_by('is_staff', 'pk',)
    # queryset.group_by= ['is_staff']
    serializer_class = AdminPanelSerializer

class AddConsultantViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    queryset = User.objects.filter(id=0)
    serializer_class = CreateConsultantSerializer


class AddSupporterViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    queryset = User.objects.filter(id=3)
    serializer_class = CreateSupporterSerializer

class UserViewSet(viewsets.ViewSet):
    # print ("*******************")
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        user= Token.objects.get(key=request.auth)
        # print (',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', user.user)
        queryset= User.objects.get(username=user.user)
        print ("sdfghjsdfghjsjksdfghjsdfjk",queryset.id)
        serializer=UserTokenSerializer(queryset)
        return Response(serializer.data)

class SupporterDetailViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(role= 'supporter')
    serializer_class = SupporterDetailSerializer




