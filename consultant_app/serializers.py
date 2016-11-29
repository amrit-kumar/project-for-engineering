from .models import *
from rest_framework import serializers
from collections import OrderedDict
from rest_framework.fields import SkipField
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.Serializer):
    class Meta:
        model= User


# class ProjectSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model= Project
#         fields=( 'pk','title',)
#         ordering = ('pk',)
#
class AdminPanelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = [field for field in self.fields.values() if not field.write_only]

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            if attribute is not None:
                represenation = field.to_representation(attribute)
                if represenation is None:
                    # Do not seralize empty objects
                    continue
                if isinstance(represenation, list) and not represenation:
                    # Do not serialize empty lists
                    continue
                ret[field.field_name] = represenation

        return ret

    class Meta:
        model= User
        # fields=('id', 'username', 'is_staff', 'current_location',)

class CreateConsultantSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            gender=validated_data['gender'],
            role=validated_data['role'],

            employee_id=validated_data['employee_id'],

            skype_username=validated_data['skype_username'],

            mobile_no=validated_data['mobile_no'],

            company_name=validated_data['company_name'],

            experience=validated_data['experience'],
            status=validated_data['status'],

            current_location=validated_data['current_location'],

            resume=validated_data['resume'],
            supporter=validated_data['supporter'],

        )
        user.set_password(validated_data['password'])
        user.save()

    class Meta:
        model= User
        exclude= ('employee_id','user_permissions','groups','is_staff', 'is_active','is_superuser')



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
        exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff', 'is_active','is_superuser','experience','company_name','date_joined')


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model= Project



class ConsultantSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ('id','username',)


class SupporterDetailSerializer(serializers.ModelSerializer):
    consultant=ConsultantSerializer
    project= ProjectSerializer


    class Meta:
        model= User
        fields=('id','username','consultant','project',)
        depth=1
        # exclude=('status','current_location','resume','supporter','user_permissions','groups','is_staff', 'is_active','is_superuser','experience','company_name','date_joined',)
#
# class TokenSerializer(serializers.Serializer):
#     user= serializers.CharField(max_length=20)

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





