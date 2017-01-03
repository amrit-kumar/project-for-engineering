from __future__ import unicode_literals
from .models import *
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_auth.serializers import PasswordResetSerializer

from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework.response import Response
from versatileimagefield.serializers import VersatileImageFieldSerializer

from django.utils import six

from rest_framework.serializers import ImageField

from versatileimagefield.utils import (
    build_versatileimagefield_url_set,
    get_rendition_key_set,
    validate_versatileimagefield_sizekey_list
)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

from .models import *
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.fields import SkipField
from . signals import *

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email',)

class SupporterSerializer(serializers.ModelSerializer):
    # supporter = serializers.SerializerMethodField('getting_supporter')
    #
    # def getting_supporter(self, obj):
    #     return obj.supporter.username

    class Meta:
        model = User

class To_do_listSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='supporter'))

    username=serializers.SerializerMethodField()

    def get_username(self,obj):
        return obj.user.username

    class Meta:
        model=To_do_list
        fields=('id','text','user','username',)

class NotificationSerializer(serializers.ModelSerializer):
    # recipient = serializers.SerializerMethodField()
    time= serializers.SerializerMethodField()
    send_by = serializers.SerializerMethodField()

    def get_send_by(self, obj):
        serializers = SenderSerializer(obj.send_by)
        return serializers.data

    def get_time(self,obj):
        return obj.timestamp

    # def get_recipient(self, obj):
    #     return obj.recipient.username

    class Meta:
        model = Notification
        fields = ('id','text','time','unread','type','comment','project','send_by')
        depth = 0

class NotificationsSerializer(serializers.ModelSerializer):
    send_by=serializers.SerializerMethodField()
    time=serializers.SerializerMethodField()

    def get_time(self,obj):
        return obj.timestamp
    def get_send_by(self, obj):
        serializers=SenderSerializer(obj.send_by)
        return serializers.data
    class Meta:
        model= Notification
        fields=('id','text','project','comment','type','unread','time','send_by',)
#
# class AdminPanelSerializer(serializers.ModelSerializer):
#     no_of_supporters = serializers.SerializerMethodField()
#     no_of_consultant = serializers.SerializerMethodField()
#     no_of_projects = serializers.SerializerMethodField()
#     comment = serializers.SerializerMethodField('getting_comment')
#     notification = serializers.SerializerMethodField('getting_notification')
#     # notification= NotificationSerializer(many=True)
#     to_do_list= serializers.SerializerMethodField('getting_to_do_list')
#
#     def get_no_of_supporters(self, obj):
#         abc = User.objects.filter(role='supporter').count()
#         return abc
#
#     def get_no_of_projects(self, obj):
#         abc = Project.objects.all().count()
#         return abc
#
#     def get_no_of_consultant(self, obj):
#         abc = User.objects.filter(role='consultant').count()
#         return abc
#
#     def getting_comment(self, obj):
#         comment = Comment.objects.filter(supporter_id=1)
#         l = []
#         for i in comment:
#             comment = Comment.objects.filter(project=i.project)
#             l.append(comment)
#         try:
#             abc = l[0]
#             serializers = CommentDetailSerializer(abc, many=True)
#             return serializers.data
#         except:
#             return None
#
#
#     def getting_notification(self, obj):
#         user = User.objects.get(id=1)
#         last_login = user.log_out_time
#         data = Notification.objects.filter(timestamp__range=(last_login, datetime.now())).filter(recipient_id=1).order_by('-timestamp')
#         serializers = NotificationsSerializer(data, many=True)
#         return serializers.data
#
#     # def getting_comment(self, obj):
#     #     return obj.comment.values_list('text', flat=True)
#     # '''.latest('comment_time') '''
#
#     def getting_to_do_list(self, obj):
#         serializers=To_do_listSerializer(obj.to_do_list,many=True)
#         return serializers.data
#
#     '''.latest('comment_time') '''
#
#     class Meta:
#
#         model= User
#         fields= ('no_of_supporters','no_of_consultant','no_of_projects','comment','notification','to_do_list',)

class SupporterPanelSerializer(serializers.ModelSerializer):
        no_of_supporters = serializers.SerializerMethodField()
        no_of_consultant = serializers.SerializerMethodField()
        no_of_projects = serializers.SerializerMethodField()
        comment = serializers.SerializerMethodField('getting_comment')
        # notification = NotificationSerializer(many=True)
        notification = serializers.SerializerMethodField('getting_notification')
        to_do_list = serializers.SerializerMethodField('getting_to_do_list')

        def get_no_of_supporters(self, obj):
            abc = User.objects.filter(role='supporter').count()
            return abc

        def get_no_of_projects(self, obj):
            abc = Project.objects.all().count()
            return abc

        def get_no_of_consultant(self, obj):
            abc = User.objects.filter(role='consultant').count()
            return abc
        def getting_comment(self, obj):
            comment = Comment.objects.filter(supporter_id=obj.id)
            l = []
            for i in comment:
                comment = Comment.objects.filter(project=i.project).order_by('-comment_time')
                l.append(comment)
            try:
                abc = l[0]
                serializers = CommentDetailSerializer(abc, many=True)
                return serializers.data
            except:
                return None
        def getting_notification(self, obj):
            user = User.objects.get(id=obj.id)
            last_login = user.log_out_time
            data = Notification.objects.filter(timestamp__range=(last_login, datetime.now())).filter(recipient_id=obj.id).order_by('-timestamp')
            serializers = NotificationsSerializer(data, many=True)
            return serializers.data

        # def getting_notification(self, obj):
        #     return obj.notification.text

        def getting_to_do_list(self, obj):
            serializers = To_do_listSerializer(obj.to_do_list,many=True)
            return serializers.data
        '''.latest('comment_time') '''

        class Meta:
            model = User
            fields = ('id', 'username','no_of_supporters','no_of_consultant','no_of_projects', 'comment', 'notification', 'to_do_list','resume',)




class SupportSerializer(serializers.ModelSerializer):
    # id = serializers.SerializerMethodField()
    def get_id(self, obj):
        return obj.id
    class Meta:
        model=User
        fields=('id','username',)

class CreateConsultantSerializer(serializers.ModelSerializer):
    # supporter = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='supporter'))
    image=VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('small', 'thumbnail__50x50'),
            ('medium', 'thumbnail__125x125'),
            ('large', 'thumbnail__260x260'),
            ('extra_large', 'thumbnail__500x500'),

            ('small_squ_crop', 'crop__260x260'),
        ], required=False,
        allow_empty_file=True,
    )
    project_list = serializers.SerializerMethodField()
    _supporter = serializers.SerializerMethodField('getting__supporter')

    def get_project_list(self, obj):
        data = Project.objects.filter(consultant=obj)
        serializers = ProjectSerializer(data, many=True)
        return serializers.data

    def getting__supporter(self, obj):
        serializers = SupportSerializer(obj.supporter)
        return serializers.data
    class Meta:
        model= User
        exclude= ('employee_id','user_permissions','groups','is_staff', 'is_active','password',)
        extra_kwargs = {
            'supporter': {'write_only': True},
            # 'image_ppoi': {'write_only': True},
        }


class RegistrationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],

            gender=validated_data['gender'],
            role=validated_data['role'],

            employee_id=validated_data['employee_id'],

            skype_username=validated_data['skype_username'],

            mobile_no=validated_data['mobile_no'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    is_active= serializers.SerializerMethodField('get_status')


    def get_status(self,obj):
        obj.is_active = False
        return obj.is_active

    class  Meta:
        model= User
        exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff', 'is_active','is_superuser','experience','company_name','date_joined',)


# class ModifyUserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model= User
#         read_only_fields=('username', 'password',)

class CreateSupporterSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],

            gender=validated_data['gender'],
            role=validated_data['role'],

            employee_id=validated_data['employee_id'],

            skype_username=validated_data['skype_username'],

            mobile_no=validated_data['mobile_no'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    class  Meta:
        model= User
        exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff','is_superuser','experience','company_name','date_joined',)
 # class ReplySerializer(serializers.ModelSerializer):
#     supporter = serializers.SerializerMethodField('getting_supporter')
#
#     def getting_supporter(self, obj):
#         return obj.supporter.username
#     class Meta:
#         model= Reply
#         fields=('reply','reply_time','supporter',)

class CommentDetailSerializer(serializers.ModelSerializer):
    # supporter=SupportSerializer()
    _supporter = serializers.SerializerMethodField()

    def get__supporter(self, obj):
        serializers = SupportSerializer(obj.supporter)
        return serializers.data

    class Meta:
        model = Comment
        fields = ('id','text', 'comment_time', '_supporter', 'project')
        ordering=(('comment_time'),)

class  CommentSerializer(serializers.ModelSerializer):
    # supporter = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='supporter'))
    _supporter = serializers.SerializerMethodField()

    def get__supporter(self, obj):
        serializers = SupportSerializer(obj.supporter)
        return serializers.data

    class Meta:
        model = Comment
        extra_kwargs = {
            'supporter': {'write_only': True},
        }


class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        # fields = ('id','username',)


class CreateProjectSerializer(serializers.ModelSerializer):
    # consultant = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='consultant'))
    # comment=CommentDetailSerializer(many=True)
    _consultant = serializers.SerializerMethodField()
    _supporter =serializers.SerializerMethodField()

    def get__supporter(self, obj):
        data=User.objects.filter(username=obj.consultant.supporter.username)
        serializers = SupportSerializer(data,many=True)
        return serializers.data

    def get__consultant(self, obj):
        data =User.objects.filter(username=obj.consultant.username)
        serializers=SupportSerializer(data,many=True)
        return serializers.data
    class Meta:
        model = Project
        # fields=('id','title','description','assigned_date','completion_date','_supporter','_consultant','technology','status')
        extra_kwargs = {
            'consultant': {'write_only': True},
        }


    # def get_reply(self,obj):
    #     serializers=ReplySerializer(obj.reply)
    #     return serializers.data

class ProjectInfoSerializer(serializers.ModelSerializer):
    consultant = serializers.SerializerMethodField()
    supporter = serializers.SerializerMethodField()
    # comment=CommentDetailSerializer(many=True)
    comment= serializers.SerializerMethodField()

    def get_comment(self,obj):
        data=Comment.objects.filter(project_id=obj.id).order_by('-comment_time')
        # page = self.paginate_queryset(data)
        serializers=CommentDetailSerializer(data,many=True)
        return serializers.data

    def get_supporter(self, obj):
        serializers = SupportSerializer(obj.consultant.supporter)
        return serializers.data

    def get_consultant(self, obj):
        data = {
            'id': obj.consultant.id,
            'username': obj.consultant.username,
            'company_name': obj.consultant.company_name,
            'skype_username':obj.consultant.skype_username,
            'contact': obj.consultant.mobile_no,
            'email': obj.consultant.email
        }
        return data

    class Meta:
        model=Project
        fields=('id','title','description','assigned_date','completion_date','supporter','consultant','comment',)

class ConsultantInfoSerializer(serializers.ModelSerializer):
    # project = ProjectInfoSerializer(many=True)
    username = serializers.SerializerMethodField('get_consultant')

    def get_consultant(self, obj):
        return obj.username

    class Meta:
        model = User
        fields = ('id', 'username','assigned_date',)
        ordering= (('assigned_date',))


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model=Technology
class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        # depth=1
        fields=('username',)

class SkillSetSerializer(serializers.ModelSerializer):

    technology_name = serializers.SerializerMethodField('get_tech')

    def get_tech(self,obj):
        return obj.technology.technology
    # def get_tech(self, obj):
    #     serializers=TechnologySerializer(obj.technology)
    #     return serializers.data

    class Meta:
        model=SkillSet
        # fields=('technology','pointer',)

class ProjectSerializer(serializers.ModelSerializer):
    # comment=CommentDetailSerializer(many=True)
    technology= serializers.SerializerMethodField()
    consultant=serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    def get_technology(self,obj):
        return obj.technology.technology
    def get_comment(self, obj):
        data = Comment.objects.filter(project_id=obj.id).order_by('-comment_time')
        serializers = CommentDetailSerializer(data, many=True)
        return serializers.data
    def get_consultant(self,obj):
        data={'id':obj.consultant.id,
              'name': obj.consultant.username}
        return data
    class Meta:
        model=Project
        fileds=('title','technology',)


class SupporterDetailSerializer(serializers.ModelSerializer):
    consultant = ConsultantInfoSerializer(read_only=True,many=True)
    username = serializers.SerializerMethodField('getting_supporter')
    skillset=SkillSetSerializer(many=True)
    # skillset = serializers.PrimaryKeyRelatedField(many=True, queryset=SkillSet.objects.all(), required=False)
    project_list = serializers.SerializerMethodField()

    def get_project_list(self, obj):
        data = Project.objects.filter(consultant__supporter=obj)
        serializers = ProjectSerializer(data, many=True)
        return serializers.data
    def getting_supporter(self, obj):
        return obj.username

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.role = validated_data.get('role', instance.role)
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.skype_username = validated_data.get('skype_username', instance.skype_username)
        instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.status = validated_data.get('status', instance.status)
        instance.assigned_date = validated_data.get('assigned_date', instance.assigned_date)
        instance.current_location = validated_data.get('current_location', instance.current_location)
        instance.resume = validated_data.get('resume', instance.resume)

        instance.supporter = validated_data.get('supporter', instance.supporter)
        skillset = validated_data.get('skillset')
        # skillset = validated_data.pop('skillset')
        #
        for skillset in skillset:
            # print(skillset)
            skillset, created = SkillSet.objects.get_or_create(pointer=skillset['pointer'],
                                                               technology=skillset['technology'],
                                                               supporter=skillset['supporter'])
            instance.skillset.add(skillset)

        return instance
        # skillset = validated_data.pop('skillset')
        #
        # for skillset in skillset:
        #     skillset, created = SkillSet.objects.get_or_create(name=skillset['name'])
        #     instance.ingredients.add(skillset)

        instance.save()
        return instance
    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name','skype_username','email','employee_id','gender','role','designation','mobile_no','experience','is_superuser','assigned_date','skillset','consultant','project_list',)
        read_only_fields=('username','email',)
        order_by= ('-assigned_date')
        depth = 1


class NoUseSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=25)

class ActiveSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        exclude= ('password',)


class NotificationDetailSerializer(serializers.ModelSerializer):
    send_by = serializers.SerializerMethodField()
    time= serializers.SerializerMethodField()

    def get_time(self, obj):
        return obj.timestamp

    def get_send_by(self, obj):
        serializers = SenderSerializer(obj.send_by)
        return serializers.data
    class Meta:
        model= Notification
        fields = ('id','text','time','unread','type','comment','project','send_by',)
        depth = 0