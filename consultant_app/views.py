from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import *
from rest_framework.decorators import *
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_auth.registration.views import LoginView
from django.shortcuts import redirect
from rest_framework import filters
from django.contrib.auth.hashers import make_password
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
import os
from consultant_app.error_codes import *
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
import redis
from rest_framework.views import APIView
from rest_framework import generics
from django.db.models import Q
from functools import reduce
import barcode
from barcode.writer import ImageWriter
import pyqrcode





class UserPermissionsObj(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj == request.user
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class SupporterPanelViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(role='supporter').filter(is_active=True)
    serializer_class = SupporterPanelSerializer

    @detail_route(methods=["GET", "POST"])
    def delete_user(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
            if user.is_superuser == True:
                return Response("User Is Admin So Cannot Be Deleted", status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if user.role == 'consultant':
                    user.delete()
                    data=User.objects.filter(role='consultant')
                    serializers=CreateConsultantSerializer(data,many=True)
                    return Response(serializers.data, status=status.HTTP_200_OK)
                else:
                    if user.role== 'supporter':
                        user.delete()
                        data = User.objects.filter(role='supporter')
                        serializers = SupporterDetailSerializer(data, many=True)
                        return Response(serializers.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404("No User matches the given query.")


    @detail_route(methods=["GET", "POST"])
    def delete_project(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            project.delete()
            return Response("Project deleted", status=status.HTTP_200_OK)

        except Project.DoesNotExist:
            raise Http404("No Project matches the given query.")


    @detail_route(methods=["GET", "POST"])
    def delete_to_do_list(self, request, pk=None):
        try:
            to_do_list = To_do_list.objects.filter(user_id=request.user.id).get(id=pk)
            to_do_list.delete()
            data = To_do_list.objects.filter(user_id=request.user.id)
            serializers = To_do_listSerializer(data, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)

        except To_do_list.DoesNotExist:
            raise Http404("No to_do_list matches the given query.")

    @detail_route(methods=["GET", "POST"])
    def delete_notification(self, request, pk=None):
        try:
            notification = Notification.objects.filter(recipient_id=request.user.id).get(id=pk)
            notification.delete()
            data = Notification.objects.filter(recipient_id=request.user.id)
            serializers = NotificationSerializer(data, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)

        except Notification.DoesNotExist:
            raise Http404("No notification matches the given query.")

    @detail_route(methods=["GET", "POST"])
    def active_user(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            user.is_active=True
            user.save()
            data = User.objects.filter(id=pk)
            serializers = SupporterDetailSerializer(data, many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise Http404("No user matches the given query.")


class AddConsultantViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # parser_classes = (MultiPartParser, FormParser, )
    queryset = User.objects.filter(role='consultant')
    serializer_class = CreateConsultantSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('first_name',)
    filter_fields = ('first_name',)

    def create(self, request):
        serializer = CreateConsultantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            value=serializer.data['resume']
            # new_dict.update({'resume_name':os.path.basename(serializer.data['resume'])})
            return Response({'message':'success'})
        else:
            if  str(serializer.errors).find("This field may not be blank."):
                return Response(HTTP_USER_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSupporterViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    # parser_classes = (MultiPartParser, FormParser, )
    queryset = User.objects.filter(id=0)
    serializer_class = CreateSupporterSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     token, created = Token.objects.get_or_create(user=serializer.instance)
    #     user = User.objects.filter(user=serializer.instance)
    #     return Response({'token': token.key, 'id': user.id}, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request,):
            if request.data['username'] == '' and request.data['email'] == '':
                return Response(HTTP_DATA_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
            elif request.data['username']=='':
                return Response(HTTP_USER_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
            elif request.data['email'] == '':
                return Response(HTTP_EMAIL_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = CreateSupporterSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 'Success'})
                else:
                     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProjectViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    queryset = Project.objects.all()
    serializer_class = CreateProjectSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('title',)
    filter_fields = ('title',)

    def create(self, request):
        project= Project.objects.filter(title=request.data['title'])
        if project.exists():
            return Response(HTTP_TITLE_NOT_VALID,status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CreateProjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # user = User.objects.get(username='amrit')
                # r = redis.StrictRedis(host='localhost', port=6379, db=0)

                # pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
                # r = redis.Redis(connection_pool=pool)

                # r.publish('chat', user.username + ': ' + "hi")
                # print("**********************",r)
                return Response({'status': 'Success'})
            else:
                return Response(HTTP_DATA_NOT_VALID,status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['GET', 'POST'])
    def get_comments(self, request, pk=None):
        data = Project.objects.get(id=pk)
        serializers = ProjectInfoSerializer(data)
        data=serializers.data
        info=str(serializers.data)
        print("**********************",info)

        Channel('repeat-me').send({'info': info, 'status': True})
        return Response(data)

class SupporterDetailViewset(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    # parser_classes = (MultiPartParser, FormParser, )
    queryset = User.objects.filter(role='supporter').filter(is_active=True)
    serializer_class = SupporterDetailSerializer
    # permission_classes=(UserPermissionsObj,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('first_name',)
    filter_fields = ('first_name',)

    @list_route(methods=["POST"])
    def filter_by_tech(self, request):
        if request.method == 'POST':
            text = (request.POST['search'])
            filtered_supporter = User.objects.filter(role="supporter").filter(
                skillset__technology__technology__icontains=text).distinct()
            if filtered_supporter:
                serializer = SkillSerializer(filtered_supporter, many=True)
                return Response({"results": serializer.data, "count": filtered_supporter.count()})
            else:
                return Response(HTTP_USER_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=404)

    @detail_route(methods=["GET", "POST"])
    def delete_skillset(self, request, pk=None):
        try:
            skillset = SkillSet.objects.filter(supporter_id=request.user.id).get(id=pk)
            skillset.delete()
            data = SkillSet.objects.filter(supporter_id=request.user.id)
            serializers = SkillSetSerializer(data, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except SkillSet.DoesNotExist:
            raise Http404("No to_do_list matches the given query.")

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
        if request.data['username'] == '' and request.data['email'] == '':
            return Response(HTTP_DATA_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
        elif request.data['username'] == '':
            return Response(HTTP_USER_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
        elif request.data['email'] == '':
            return Response(HTTP_EMAIL_CANT_BE_BLANK, status=status.HTTP_400_BAD_REQUEST)
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Token.objects.get_or_create(user=serializer.instance)
            return Response({'status':'Success'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def list(self, request):
        user= Token.objects.get(key=request.auth)
        queryset= User.objects.get(username=user.user)
        serializer=UserSerializer(queryset,context={'request': request})
        return Response(serializer.data)

class LogoutViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def list(self, request):
        user = request.user
        user.log_out_time = datetime.now()
        user.save()
        Token.objects.get(user=request.user).delete()
        Token.objects.create(user=request.user)
        serializer = NoUseSerializer(request.user)
        return Response({'status':'You have been successfully logged out!'})

class GetActiveViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=False).filter(role='supporter')
    serializer_class = ActiveSerializer

    def create(self, request):
        serializer = ActiveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ModifyUser(viewsets.ViewSet):
#     def list(self, request):
#         queryset= User.objects.get(username=request.user.username)
#         serializer= ModifyUserSerializer(queryset)
#         return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(id=0)
    serializer_class = CommentSerializer
    # pagination_class = LargeResultsSetPagination

    # def create(self, request):
    #     serializers = CommentDetailSerializer(data=request.data)
    #     # serializers.save()
    #
    #     if serializers.is_valid():
    #         print("****************************************")
    #         serializers.save()
    #         print("***************",serializers.data)
    #         return Response(serializers.data)
    #     return Response(serializers.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    pagination_class = LargeResultsSetPagination


    def list(self,request):
        data=Notification.objects.all().order_by('-timestamp')
        page = self.paginate_queryset(data)

        serializers=NotificationSerializer(page,many=True)
        return Response(serializers.data)

    def retrieve(self, request, pk=None):
        data = Notification.objects.filter(recipient__id=pk).order_by('-timestamp')
        page = self.paginate_queryset(data)
        serializers = NotificationDetailSerializer(page, many=True)
        return Response(serializers.data)
    #
    # @detail_route(methods=['GET','POST'])
    # def get_notify(self,request,pk=None):
    #     data=Notification.objects.filter(recipient__id=pk).order_by('-timestamp')
    #     page = self.paginate_queryset(data)
        # serializers=NotificationDetailSerializer(page, many=True)
        # return Response(serializers.data)

class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all().order_by('technology')
    serializer_class = TechnologySerializer

class To_do_listViewSet(viewsets.ModelViewSet):
    queryset= To_do_list.objects.all()
    serializer_class = To_do_listSerializer

class HistoryViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = HistorySerializer

    @detail_route(methods=["GET", "POST"])
    def history(self,request,pk=None):

        final_list=[]
        User.objects.filter(id=pk)
        his=User.history.filter(id=pk)
        # User.role=='supporter'
        var1=User.objects.filter(id=pk)
        var3=User.objects.filter(id=pk)

        var2=Project.history.filter(consultant_id=pk)
        var4=Projec1Serializer(var2,many=True)
        hi=HistorySerializer(his,many=True)
        final_list.append(hi.data)
        final_list.append(var4.data)

        return Response(final_list)

class GlobalSearchViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = GlobalSearchSerializer
    print("((((((((((((((((((((")

    @list_route(methods=["POST"])
    def filter_by_any(self, request):
       if request.method == 'POST':
          query = (request.POST['query'])
          # query = (request.POST['search'])
          # query = self.request.query_params.get('query',None)
          snippets = User.objects.filter(username__icontains=query)
          print("********************",snippets)
          tech = User.objects.filter(skype_username__icontains=query)
          print("+++++++++++++",tech)
          # all_results.sort(key=lambda x: x.created)
          filtered_supporter = User.objects.filter(role="supporter").filter(
              skillset__technology__technology__icontains=query).distinct()
          # tech=Technology.objects.filter()
          pro=Project.objects.filter(title__icontains=query)
          print("rpoject",pro)
          var2=ProjectSerializer(pro,many=True)
          var2=var2.data
          serializ = GlobalSearchSerializer(snippets, many=True)
          serializ=serializ.data
          serializ1 = GlobalSearchSerializer(tech, many=True)
          serializ1=serializ1.data
          serializ2 = GlobalSearchSerializer(filtered_supporter, many=True)
          serializ2=serializ2.data

          all_results = list(chain(serializ, serializ1,serializ2,var2))
          unique = reduce(lambda l, x: l + [x] if x not in l else l, all_results, [])
          #to make the list of unique elements
          #or to make unique we can use Q objects in django

          # s = set(val for dic in all_results for val in dic.values())
          print("TTTTTTTTTTTTTTTTTTT",type(unique))
          print("&&&&&&&&&&&&&&&&&",unique)
          # var = serializ.data


          return Response(unique)
