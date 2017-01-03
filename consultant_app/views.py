import sys
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
from rest_framework.parsers import MultiPartParser, FormParser,FileUploadParser
from PIL import Image
from ws4redis.publisher import RedisPublisher



class UserPermissionsObj(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return obj == request.user
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000

# class AdminPanelViewSet(viewsets.ReadOnlyModelViewSet):
#     authentication_classes = (TokenAuthentication,)
#     # permission_classes = (IsAdminUser)
#     queryset = User.objects.filter(is_superuser=True)
#     serializer_class = AdminPanelSerializer
#
#     @detail_route(methods=["GET", "POST"])
#     def delete_user(self, request, pk=None):
#
#         try:
#             user = User.objects.get(pk=pk)
#             if user.is_superuser == True:
#                 return Response("User Is Admin So Cannot Be Deleted", status=status.HTTP_406_NOT_ACCEPTABLE)
#             else:
#                 user.delete()
#                 return Response("user  deleted", status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             raise Http404("No User matches the given query.")
#
#
#     @detail_route(methods=["GET", "POST"])
#     def delete_project(self, request, pk=None):
#         try:
#             project = Project.objects.get(pk=pk)
#             project.delete()
#             return Response("Project deleted", status=status.HTTP_200_OK)
#
#         except Project.DoesNotExist:
#             raise Http404("No Project matches the given query.")
#
#
#     @detail_route(methods=["GET", "POST"])
#     def delete_to_do_list(self, request, pk=None):
#         try:
#             to_do_list = To_do_list.objects.filter(user_id=1).filter(id=pk)
#             to_do_list.delete()
#             data = To_do_list.objects.filter(user_id=1)
#             serializers=To_do_listSerializer(data,many=True)
#             return Response(serializers.data,status=status.HTTP_200_OK)
#
#         except Project.DoesNotExist:
#             raise Http404("No to_do_list matches the given query.")

class SupporterPanelViewSet(viewsets.ReadOnlyModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(role='supporter')
    serializer_class = SupporterPanelSerializer

    @detail_route(methods=["GET", "POST"])
    def delete_user(self, request, pk=None):

        try:
            user = User.objects.get(pk=pk)
            if user.is_superuser == True:
                return Response("User Is Admin So Cannot Be Deleted", status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                user.delete()
                data=User.objects.all()
                serializers=SupporterDetailSerializer(data,many=True)
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

class AddConsultantViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
    parser_classes = (MultiPartParser, FormParser,FileUploadParser,)
    queryset = User.objects.filter(role='consultant')
    serializer_class = CreateConsultantSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('first_name',)
    filter_fields = ('first_name',)

    # def post(self, request, filename, format=None):
    #     file_obj = request.POST['resume']
    #     print("hiiiiiiiiii there",file_obj)
    #     # do some stuff with uploaded file
    #     return Response(status=204)

    def create(self, request):
        serializer = CreateConsultantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSupporterViewSet(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAdminUser,)
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
        serializer = CreateProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Success'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['GET', 'POST'])
    def get_comments(self, request, pk=None):
        queryset = Project.objects.filter(id=pk)
        serializers = ProjectInfoSerializer(queryset, many=True)
        data=serializers.data
        return Response(data.pop(0))
class SupporterDetailViewset(viewsets.ModelViewSet):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(role='supporter')
    serializer_class = SupporterDetailSerializer
    permission_classes=(UserPermissionsObj,)
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('first_name',)
    filter_fields = ('first_name',)

    @list_route(methods=["POST"])
    def filter_by_tech(self, request):
        if request.method == 'POST':
            text = (request.POST['search'])
            filtered_supporter = User.objects.filter(role="supporter").filter(
                skillset__technology__technology__icontains=text).distinct()
            serializer = SkillSerializer(filtered_supporter, many=True)
            return Response({"results": serializer.data, "count": filtered_supporter.count()})
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
        serializer = UserSerializer(queryset, context={'request': request})
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

    # @detail_route(methods=['GET','POST'])
    # def get_list(self,request,pk=None):
    #     data=To_do_list.objects.filter(user=pk)
    #     serializers=To_do_listSerializer(data,many=True)
    #     return Response(serializers.data)




# # class LoginViewCustom(LoginView):
#         authentication_classes = (TokenAuthentication,)
# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#     def list(self, request):
#         data=User.objects.get(username=request.auth.user.username)
#         serializers=UserSerializer(data)
#         return Response(serializers.data)
class SomeCustomSizedImageCls:
    pass
