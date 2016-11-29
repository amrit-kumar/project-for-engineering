from .models import *
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.fields import SkipField
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.Serializer):
    class Meta:
        model= User


class AdminPanelSerializer(serializers.ModelSerializer):

    comment = serializers.SerializerMethodField('getting_comment')
    notification= serializers.SerializerMethodField('getting_notification')
    to_do_list= serializers.SerializerMethodField('getting_to_do_list')
    def getting_comment(self, obj):
        return obj.comment.values_list('content', flat=True)
    '''.latest('comment_time') '''

    def getting_notification(self, obj):
        return obj.notification.values_list('content', flat=True)

    '''.latest('comment_time') '''

    def getting_to_do_list(self, obj):
        return obj.to_do_list.values_list('content', flat=True)

    '''.latest('comment_time') '''

    class Meta:

        model= User
        fields= ('comment','notification','to_do_list',)


class CreateConsultantSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        exclude= ('user_permissions','groups','is_staff', 'is_superuser', 'password',)
        # extra_kwargs = {'password': {'write_only': True}, }


class CreateSupporterSerializer(serializers.ModelSerializer):

    class  Meta:
        model= User
        exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff', 'is_superuser','experience','company_name','date_joined','password',)
        # extra_kwargs = {'password': {'write_only': True}, }

# class RegisterConsultantSerializer(serializers.ModelSerializer):
#     is_active = serializers.SerializerMethodField('get_status')
#
#     def get_status(self, obj):
#         obj.is_active = False
#
#         return obj.is_active
#     class Meta:
#         model= User
#         exclude= ('user_permissions','groups','is_staff','is_superuser', 'password','is_active',)

class RegisterSupporterSerializer(serializers.ModelSerializer):
    is_active = serializers.SerializerMethodField('get_status')

    def get_status(self, obj):
        obj.is_active = False

        return obj.is_active
    class  Meta:
        model= User
        exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff', 'is_superuser','experience','company_name','date_joined','password','is_active',)


class CommentDetailSerializer(serializers.ModelSerializer):
    supporter = serializers.SerializerMethodField('getting_supporter')

    def getting_supporter(self, obj):
        return obj.supporter.username

    class Meta:
     model=Comment
     exclude=('project',)

class ProjectInfoSerializer(serializers.ModelSerializer):
     comment= CommentDetailSerializer(many=True)
     class Meta:
         model=Project
         fields=('id','title','description','assigned_date','completion_date','comment',)
    #
class ConsultantInfoSerializer(serializers.ModelSerializer):
    project = ProjectInfoSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username','project',)


class SupporterDetailSerializer(serializers.ModelSerializer):
    consultant = ConsultantInfoSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'consultant')
        depth = 1


class UserTokenSerializer(serializers.Serializer):
    username= serializers.CharField(max_length=30)
    first_name= serializers.CharField(max_length=30)
    last_name= serializers.CharField(max_length=30)
    email= serializers.EmailField()
    gender= serializers.CharField(max_length=30)
    role= serializers.CharField(max_length=30)
    employee_id= serializers.CharField(max_length=30)
    skype_username= serializers.CharField(max_length=30)
    mobile_no= serializers.CharField(max_length=30)
    company_name= serializers.CharField(max_length=30)
    experience= serializers.CharField(max_length=30)
    current_location= serializers.CharField(max_length=30)
    status= serializers.CharField(max_length=30)
    resume= serializers.FileField()
    supporter= serializers.PrimaryKeyRelatedField(read_only=True)


class CreateProjectSerializer(serializers.ModelSerializer):

     class Meta:
        model = Project


class NoUseSerializer(serializers.Serializer):
    username= serializers.CharField(max_length=20)



class ActivateUserSerializer(serializers.ModelSerializer):


    class Meta:
        model= User
        fields= ('username', 'email', 'role', 'is_active',)
        read_only_fields= ('username', 'email', 'role',)

