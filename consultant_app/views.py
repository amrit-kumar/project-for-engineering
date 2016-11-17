from django.shortcuts import render
# from rest_auth.registration import *
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from django.http import HttpResponse
from .models import *
from .serializers import  *
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import detail_route

# class TokenTest(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request, format=None):
#         return Response({'detail': "I suppose you are authenticated"})


# class ConsultantViewset(viewsets.ModelViewSet):
#
#     # authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAuthenticated,)
#     queryset = Token.objects.get(user=request.user.id)
#     serializer_class = TokenAuthentication


class AdminPanelViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Consultant.objects.all()
    serializer_class = AdminPanelSerializer
