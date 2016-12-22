
# Create your tests here.

from django.test import TestCase
from consultant_app.models import *
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .views import *
from django.test import Client
from django.test.utils import setup_test_environment
from datetime import datetime



# class SupporterTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@…', password='top_secret')
#         Supporter.objects.create(user=User.objects.get(username='jacob'),email='email1@gmail.com' , skype_username='email1',   mobile_no='68468168')
#         # Supporter.objects.create(user=User(),email='email2@gmail.com' , skype_username='email2',   mobile_no='635465151')
#
#     def testsetup1(self):
#         pass
#         emailuser1=Supporter.objects.all()
#         print("emailuser****************************",emailuser1)
#         print("emailuserr comment &&&&&&&&&&&&&&&&&&&&&&&&&",emailuser1.filter( skype_username='email1'))
#         # emailuser2=Supporter.objects.get(skype_username='email2')
        # self.assertContains(emailuser1.comment_set,'comment ')


        # self.assertEqual(emailuser2.comment_set.all(),'comment set so second test case passed')
#

class ProjectTestCase(TestCase):
    # def setUp(self):
    #     self.factory = RequestFactory()
    #     Project.objects.create(project_description='first project')
    #     Project.objects.create(project_description='second project')

    def testsetup2(self):
        client = Client()
        response = client.get('/project/project_comment')
        print("response content **************",response.content)
        # print("response.contexttttttttttttttttttttttttt",response.context[''])
        # request = self.factory.get(project_description='movie booking app')
        # request.user = self.user
        # response = ProjectViewset.project_comment(request)
        self.assertEqual(response.status_code, 301)

        # objectget1=Project.objects.get(project_description='first project')
        # print("objectget11111111111111111111111111111111",objectget1)
        # objectget2=Project.objects.get(project_description='second project')
        # self.assertAlmostEqual(objectget1.available_comments,'comment')
        # self.assertEqual(objectget2.completion_date,'available_comments 2')
    def testsetup3(self):
        obj=Project.objects.create(project_description='second project')
        time=datetime.now()
        print("tiiiiiiiiiiiiiiiimmmmmmmmmmmmmmmmeeeeeeeeeeeeee",datetime.astimezone())
        self.assertEqual(obj.assigned_date,datetime.now())



