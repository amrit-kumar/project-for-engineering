from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from .models import *
from .serializers import  *
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.hashers import make_password
from rest_auth.registration.views import LoginView
from rest_auth.views import PasswordResetView


class AdminPanelHomePageViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    queryset = User.objects.filter(is_superuser=True)
    # queryset.group_by= ['is_staff']
    serializer_class = AdminPanelSerializer

class AddConsultantViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    # def perform_create(self, serializer):
    #     password = make_password(self.request.data['password'])
    #
    #     serializer.save(password=password)

    queryset = User.objects.filter(role= 'consultant')
    serializer_class = CreateConsultantSerializer


class AddSupporterViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    # def perform_create(self, serializer):
    #     password = make_password(self.request.data['password'])
    #
    #     serializer.save(password=password)
    queryset = User.objects.filter(role= 'supporter')
    serializer_class = CreateSupporterSerializer

class UserViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        user= Token.objects.get(key=request.auth)
        # print (',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', user.user)
        queryset= User.objects.get(username=user.user)
        # print ("sdfghjsdfghjsjksdfghjsdfjk",queryset.id)
        serializer=UserTokenSerializer(queryset)
        return Response(serializer.data)

class SupporterDetailViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(role= 'supporter')
    serializer_class = SupporterDetailSerializer


class AddProjectViewSet(viewsets.ModelViewSet):
     queryset = Project.objects.filter(id=0)
     serializer_class = CreateProjectSerializer


class LogoutViewSet(viewsets.ViewSet):
    def list(self, request):
        Token.objects.get(user= request.user).delete()
        Token.objects.create(user= request.user)
        serializer= NoUseSerializer(request.user)
        return serializer.data




class SupporterRegisterViewSet(viewsets.ModelViewSet):

    queryset = User.objects.filter(id=0)
    serializer_class = RegisterSupporterSerializer

class ActivateUser(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    queryset = User.objects.filter(is_active=False)
    serializer_class = ActivateUserSerializer

