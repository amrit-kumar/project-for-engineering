# from __future__ import unicode_literals
#
# import os
# import re
# import sys
# import magic
# from .models import *
#
# from django.core.exceptions import ValidationError
# from django.utils import six
# from django.utils.deconstruct import deconstructible
# from django.utils.encoding import force_text
# from django.utils.functional import SimpleLazyObject
# from django.utils.ipv6 import is_valid_ipv6_address
# from rest_framework.validators import UniqueValidator
# # from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit
# from django.utils.translation import ugettext_lazy as _, ungettext_lazy
# from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
# from django.dispatch import receiver
#
# EMPTY_VALUES = (None, '', [], (), {})
#
# # @receiver(post_save, sender=None)
def validate_file_extension(fieldfile_obj,**kwargs):
    pass
#
#     # time--7.22
#
#
#     from .models import User,get_attachment_file_path
#
#     megabyte_limit = 5.0  # in BYTE
#     file_path=get_attachment_file_path(instance=fieldfile_obj,filename=str(fieldfile_obj))
#     name=str(fieldfile_obj)
#     print("name of file -",name)
#
#     print("actual file_path -",file_path)
#     ac_name=file_path.split('/')[-1]
#     print("actual_name-",ac_name)
#     # print("size of file in byte -", fieldfile_obj._size)
#     file_size=888888888888888888888888888888888888888
#
#     import magic
#     magic._get_magic_type(mime=True)
#     # magic.from_file(filename=name,mime=False)
#     print("____________________",magic._get_magic_type(mime=False))
#     url="/home/consultadd/Desktop/" + name
#
#     size_of_object = sys.getsizeof(fieldfile_obj)
#     print("size_of_object",size_of_object)
#
#     ext = os.path.splitext(fieldfile_obj.name)[1]  # [0] returns path+filename
#     print("extension",ext)
#     valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls','.txt','.odt','.gif']
#
#     # project_url = "/home/consultadd/Desktop/workspace/tixdo_space/uttu_project/my_project/user/" + ac_name
#     # print("++++++++++++++++++++++++", magic.from_file(file_path, mime=True))
#
#     if not ext.lower() in valid_extensions:
#
#         raise ValidationError(u'Unsupported file extension.')
#
#     # elif file_size > megabyte_limit*1024*1024:
#     else:
#
#         raise ValidationError("Max file size is %s Byte" % str(megabyte_limit))
#
#
#
#
# @deconstructible
# class FileExtensionValidator(object):
#     message = _(
#         "File extension '%(extension)s' is not allowed. "
#         "Allowed extensions are: '%(allowed_extensions)s'."
#     )
#     code = 'invalid_extension'
#     valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls']
#     def __init__(self, allowed_extensions=valid_extensions, message=None, code=None):
#         self.allowed_extensions = allowed_extensions
#         if message is not None:
#             self.message = message
#         if code is not None:
#             self.code = code
#
#     def __call__(self, value):
#         extension = os.path.splitext(value.name)[1][1:].lower()
#         if self.allowed_extensions is not None and extension not in self.allowed_extensions:
#             raise ValidationError(
#                 self.message,
#                 code=self.code,
#                 params={
#                     'extension': extension,
#                     'allowed_extensions': ', '.join(self.allowed_extensions)
#                 }
#             )
#
#     def __eq__(self, other):
#         return (
#             isinstance(other, self.__class__) and
#             self.allowed_extensions == other.allowed_extensions and
#             self.message == other.message and
#             self.code == other.code
#         )