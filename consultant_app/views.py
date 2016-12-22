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
from rest_framework import status
from django.db.models import Q
import django_filters
from rest_framework import filters
from django.shortcuts import get_object_or_404
from django.http import Http404
from datetime import datetime, timedelta, date
import datetime
from django.contrib.auth.models import update_last_login
from rest_framework.filters import DjangoFilterBackend
from .filters import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.template import RequestContext
from django.shortcuts import render_to_response
import requests
from django.contrib.contenttypes.models import ContentType
from rest_framework.pagination import PageNumberPagination



class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000






class AdminPanelHomePageViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    queryset = User.objects.filter(is_superuser=True)
    # queryset.group_by= ['is_staff']
    serializer_class = AdminPanelSerializer


    # @list_route(methods=["GET"])
    # def admin_panel_fun(self, request):
    #     dict={}
    #
    #     no_of_supporters = User.objects.filter(role='supporter').count()
    #     dict["no_of_supporters"] = no_of_supporters
    #
    #     no_of_consultant = User.objects.filter(role='consultant').count()
    #     dict["no_of_consultant"] = no_of_consultant
    #
    #     no_of_projects = Project.objects.all().count()
    #     dict["no_of_projects"] = no_of_projects
    #
    #
    #     comment = Comment.objects.filter(supporter__is_superuser=True)
    #     ser1 = Comment1Serializers(comment, many=True)
    #     dict["available_comments"] = ser1.data
    #
    #     notification = Notification.objects.all()
    #     ser2 = Notification1Serializers(notification, many=True)
    #     dict["notifications"] = ser2.data
    #
    #     to_do_list = To_do_list.objects.filter(user__is_superuser=True)
    #     ser3=ToDoListSerializer(to_do_list,many=True)
    #     dict["ToDoListSerializer"] = ser3.data
    #
    #     return Response(dict)
    #

class AddConsultantViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)
    # def perform_create(self, serializer):
    #     password = make_password(self.request.data['password'])

    #     serializer.save(password=password)
    queryset = User.objects.filter(role= 'consultant')
    serializer_class = CreateConsultantSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('first_name',)
    filter_fields = ('first_name',)


class AddSupporterViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = CreateSupporterSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields = ('role', 'username')

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     token, created = Token.objects.get_or_create(user=serializer.instance)
    #     user = User.objects.filter(user=serializer.instance)
    #     return Response({'token': token.key, 'id': user.id}, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request):
        serializer = CreateSupporterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            token, created=Token.objects.get_or_create(user=serializer.instance)
            # user = User.objects.filter(id=serializer.instance.id)

            return Response({'token':token.key,'uid':serializer.instance.id,'status': 'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    def list(self, request):
        user= Token.objects.get(key=request.auth)
        print (',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,', user.user)
        queryset= User.objects.get(username=user.user)

        print ("sdfghjsdfghjsjksdfghjsdfjk",queryset.id)
        serializer=UserTokenSerializer(queryset)
        return Response(serializer.data)

    # def destroy(self, request, pk=None):
    #     pass
    @detail_route(methods=["GET","POST"])
    def delete_user(self,request,pk=None):

        try:
            user = User.objects.get(pk=pk)
            if user.is_superuser==True:
                return Response("User Is Admin So Cannot Be Deleted",status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                user.delete()
                user1=User.objects.all()
                return Response("user  deleted",status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404("No User matches the given query.")



    @list_route(methods=["GET"])
    def all_user_data(self,request):
        each_user=User.objects.all()
        print("*******************",each_user)
        hi=each_user.values()
        for i in hi:
             print("this is id",i['id'])
             print("this is username",i['username'])
        serializer=UserSerializer(hi,many=True)
        return Response(serializer.data)


class SupporterDetailViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(role='supporter')
    serializer_class = SupporterDetailSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # filter_class=LibraryFilter
    search_fields = ('first_name',)
    filter_fields = ('first_name',)


    @list_route(methods=["POST"])
    def filter_supporter(self,request):
        if request.method == 'POST':
            text = (request.POST['search'])
            # filtered_supporter=SkillSet.objects.filter(Q(supporter__project__technology__icontains="java")).distinct()
            filtered_supporter=User.objects.filter(role="supporter").filter(skillset__technology__technology__icontains=text).distinct()
            serializer = SkillSetSerializer(filtered_supporter, many=True)
            return Response({"results": serializer.data, "count": filtered_supporter.count()})

        else:
            return Response(status=404)

    @list_route(methods=["GET","POST"])
    def supporter_comment(self,request,pk=None):
        # user=User.objects.get(pk=pk)
        # project=Project.objects.filter()

        return Response("dfgbgienviev")







class AddProjectViewSet(viewsets.ModelViewSet):
     queryset = Project.objects.filter(id=0)
     serializer_class = CreateProjectSerializer

     def create(self, request):
         serializer = RegisterSupporterSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response({'status': 'Success'})
         else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectInfoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    @detail_route(methods=["GET","POST"])
    def delete_project(self,request,pk=None):
        try:
            project=Project.objects.get(pk=pk)
            # now = datetime.now()
            # print("Current year: %d" % now.year)
            # print("Current month: %d" % now.month)
            # print("Current day: %d" % now.day)
            print("((((((((((((((((((((((((((",datetime.date.today())
            # if project.completion_date <= date(now.year, now.month, now.day):
            if project.completion_date <= datetime.date.today():

                project.delete()
                return Response("Project  deleted but someone was working on it", status=status.HTTP_200_OK)
            else:
                return Response("cannot be deleted")

        except Project.DoesNotExist:
            raise Http404("No Project matches the given query.")

class ToDoListViewset(viewsets.ModelViewSet):
    queryset = To_do_list.objects.all()
    serializer_class = ToDoListSerializer

    @list_route(methods=["GET", "POST"])
    def add_to_do_list(self, request):
        text = (request.POST['text'])
        # print("$$$$$$$$$$$$$$$$4",text)

        var = To_do_list.objects.create(text='hiiiiiiiiiii',user=User.objects.get(id=16))
        var=ToDoListSerializer(var,many=True)
        print("***************",var,"%%%%%%%%%%%%%%%%%%%%",var.data)
        return Response(var.data)
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    # @detail_route(methods=["GET","POST"])
    # def to_do_list(self,request,pk=None):
    #     if request.method=="GET":
    #         user=To_do_list.objects.filter(user=pk)
    #         print("userrrrrrrrrrrr",user)
    #         serializer=ToDoListSerializer(user,many=True)
    #         return Response(serializer.data)
    #
    #     else:
    #         serializer = ToDoListSerializer(data=request.data)
    #         if serializer.is_valid():
    #             user = To_do_list.objects.create(
    #                 text=serializer.data['text'],
    #                 user=serializer.data['user'],
    #             )
    #             print("uuuuuuuu",user)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationViewset(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = Notification1Serializers
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)

    @detail_route(methods=["GET","POST"])
    def getting_notification(self, request,pk=None):
        user = User.objects.get(id=pk)
        last_login = user.last_login
        data = Notification.objects.filter(timestamp__range=(last_login, datetime.now()))
        print("**********************************",last_login)
        print("################################",datetime.now())
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",data)

        serializers = Notification1Serializers(data, many=True)
        return Response(serializers.data)




class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(id=0)
    serializer_class = RegistrationSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     token, created = Token.objects.get_or
    # _create(user=serializer.instance)
    #     user = User.objects.filter(user=serializer.instance)
    #     return Response({'token': token.key, 'id': user.id}, status=status.HTTP_201_CREATED, headers=headers)
    def create(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Token.objects.get_or_create(user=serializer.instance)
            return Response({'status':'Success'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class TechnologyViewset(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializers

    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = TechnologyFilter
    # context_instance = RequestContext(requests)
    # search_fields = ('first_name',)
    # filter_fields = ('first_name',)

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    # whatever you want for create/destroy/update.
    serializer_class = CommentSerializers
    retrieve_serializer_class = Comment1Serializers

    pagination_class =LargeResultsSetPagination


    def get_serializer_class(self):
        if self.action in ["update", "create"]:
            return self.serializer_class
        elif self.action in ["retrieve", "list"]:
            return self.retrieve_serializer_class

        return self.serializer_class
    @detail_route(methods=["GET","POST"])
    def comment_activity(self,request,pk=None):

        comment = Comment.objects.get(pk=pk)
        hii=Activity.objects.create(content_object=comment, activity_type=Activity.LIKE, user=request.user)
        # Get all Activity instances related to Post
        fi=comment.activities.all()
        print("###############333",fi)
        # Count the number of likes
        count=comment.activities.count()
        # Get the users who liked the post
        fii=comment.activities.values_list('user__first_name', flat=True)

        var = Comment.objects.get(pk=22)
        likes = var.activities.filter(activity_type=Activity.LIKE)
        print("activitiesactivities",likes)

        # Display how many up votes
        count = likes.count()
        print("$$$$$$$$$$$$$4",count)

        # Display the names of users who up voted
        up_voters = likes.values_list('user__username')
        print("up_voters up_voters",up_voters)

        return Response(count)




