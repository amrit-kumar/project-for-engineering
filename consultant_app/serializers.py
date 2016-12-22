from .models import *
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.fields import SkipField
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.Serializer):
    class Meta:
        model= User
        # fields= ('username','id',)



class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.SerializerMethodField()

    def get_recipient(self, obj):
        return obj.recipient.username

    class Meta:
        model= Notification
        # fields = ('id','text','timestamp','unread','recipient')
        depth = 0



class AdminPanelSerializer(serializers.ModelSerializer):
    no_of_supporters = serializers.SerializerMethodField()
    no_of_consultant = serializers.SerializerMethodField()
    no_of_projects = serializers.SerializerMethodField()

    comment = serializers.SerializerMethodField('getting_comment')
    notification= NotificationSerializer(many=True)
    to_do_list= serializers.SerializerMethodField('getting_to_do_list')

    def get_no_of_supporters(self, obj):
        abc = User.objects.filter(role='supporter').count()
        return abc

    def get_no_of_consultant(self, obj):
        abc = User.objects.filter(role='consultant').count()
        return abc

    def get_no_of_projects(self, obj):
        abc = Project.objects.all().count()
        return abc

    def getting_comment(self, obj):
        return obj.comment.values_list('text', flat=True)
    '''.latest('comment_time') '''

    def getting_to_do_list(self, obj):
        return obj.to_do_list.values_list('text', flat=True)

    '''.latest('comment_time') '''

    class Meta:

        model= User
        fields= ('no_of_supporters','no_of_consultant','comment','notification','to_do_list','no_of_projects',)

class CreateConsultantSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        exclude= ('user_permissions','groups','is_staff', 'is_superuser', 'password',)
        # extra_kwargs = {'password': {'write_only': True}, }


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
        exclude=('status','current_location','resume','supporter','user_permissions',
                 'groups','is_staff', 'is_superuser','experience','company_name','date_joined','password','is_active',)
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity

class CommentDetailSerializer(serializers.ModelSerializer):
    supporter = serializers.SerializerMethodField('getting_supporter')
    activity = ActivitySerializer(many=True)

    def getting_supporter(self, obj):
        return obj.supporter.username

    class Meta:
     model=Comment
     exclude=('project',)

class ProjectInfoSerializer(serializers.ModelSerializer):
     comment= CommentDetailSerializer(many=True)
     class Meta:
         model=Project
         fields=('id','title','description','assigned_date','completion_date','comment','activity',)
    #
class ConsultantInfoSerializer(serializers.ModelSerializer):
    project = ProjectInfoSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username','project',)

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model=SkillSet

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

class SkillSetSerializer(serializers.ModelSerializer):
    technology_name = serializers.SerializerMethodField('get_tech')

    def get_tech(self, obj):
        return obj.technology.technology

    class Meta:
        model=SkillSet
        # depth=1

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

        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name','skype_username','email','employee_id','gender','role','designation','mobile_no','experience','is_superuser','assigned_date','skillset','consultant','project_list',)
        read_only_fields=('username','email',)
        order_by= ('-assigned_date')
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

class CommentDetailSerializer(serializers.ModelSerializer):
    supporter = serializers.SerializerMethodField('getting_supporter')

    def getting_supporter(self, obj):
        return obj.supporter.username

    class Meta:
     model=Comment
     exclude=('project',)


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



class ToDoListSerializer(serializers.ModelSerializer):

    class Meta:
        model=To_do_list
        # fields=('text',)

class Notification1Serializers(serializers.ModelSerializer):
    class Meta:
        model=Notification
class SupporterSerializers(serializers.ModelSerializer):
    class Meta:
        model=User

        fields=('id','username',)

class Comment1Serializers(serializers.ModelSerializer):
    supporter=SupporterSerializers()

    class Meta:
        model=Comment
        fields = ('id', 'text', 'comment_time', 'supporter', 'project')
        
class Supporter1Serializers(serializers.ModelSerializer):
    class Meta:
        model=User

        fields=('username','id',)

class CommentSerializers(serializers.ModelSerializer):

    # _supporter=serializers.SerializerMethodField()
    #
    # def get__supporter(self,obj):
    #     serializers=Supporter1Serializers(obj.supporter)
    #     return serializers.data

    class Meta:
        model = Comment

        # fields = ('id', 'text','comment_time', 'project', '_supporter',)

        # extra_kwargs = {
        #     'supporter': {'write_only': True},
        # }

class RegistrationSerializer(serializers.ModelSerializer):
    is_active= serializers.SerializerMethodField('get_status')


    def get_status(self,obj):
        obj.is_active = False
        return obj.is_active

    class  Meta:
        model= User
        exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff', 'is_active','is_superuser','experience','company_name','date_joined',)

class TechnologySerializers(serializers.ModelSerializer):
    class Meta:
        model = Technology

