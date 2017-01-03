from consultant_app.models import *
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from .views import *
from django.test import Client
from django.test.utils import setup_test_environment
from datetime import datetime
from rest_framework.test import APIRequestFactory
from django.http import HttpResponse
from rest_framework import status




class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.to_do_list = To_do_list.objects.create_to_do_list(
            text='new test text')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/to_do_list')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        # request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        # response = my_view(request)
        # Use this syntax for class-based views.
        response = To_do_listViewSet.as_view({'get'})
        print("****************",response)
        self.assertEqual(response.status_code, 200)

class Api_Test_Case(TestCase):
    def testsetup1(self):
        client = Client()
        response = client.get('/add_project')
        print("response content for testsetup 111111111111",response)
        self.assertEqual(response.status_code, 301)

    def testsetup2(self):
        client = Client()
        response = client.get('/supporter_panel')
        print("response content for testsetup 222222222222",response)
        self.assertEqual(response.status_code, 301)

    def testsetup3(self):
        client = Client()
        response = client.get('/add_consultant')
        print("response content for testsetup 333333333333",response)
        self.assertEqual(response.status_code, 301)

    def testsetup4(self):
        client = Client()
        response = client.get('/add_supporter')
        print("response content for testsetup 44444444444",response)
        self.assertEqual(response.status_code, 301)

    def testsetup5(self):
        client = Client()
        response = client.get('/add_project')
        print("response content for testsetup 55555555555",response)
        self.assertEqual(response.status_code, 301)

    def testsetup6(self):
        client = Client()
        response = client.get('/supporter')
        print("response content for testsetup 6666666666",response)
        self.assertEqual(response.status_code, 301)

    def testsetup7(self):
        client = Client()
        response = client.get('/logout')
        print("response content for testsetup 7777777777",response)
        self.assertEqual(response.status_code, 301)

    def testsetup8(self):
        client = Client()
        response = client.get('/register')
        print("response content for testsetup 8888888888",response)
        self.assertEqual(response.status_code, 301)

    def testsetup9(self):
        client = Client()
        response = client.get('/log')
        print("response content for testsetup 9999999999", response)
        self.assertEqual(response.status_code, 301)

    def testsetup10(self):
        client = Client()
        response = client.get('/active')
        print("response content for testsetup 1000000000", response)
        self.assertEqual(response.status_code, 301)

    def testsetup11(self):
        client = Client()
        response = client.get('/notification')
        print("response content for testsetup 11 11 11 11 11", response)
        self.assertEqual(response.status_code, 301)

    def testsetup12(self):
        client = Client()
        response = client.get('/technology')
        print("response content for testsetup 1212121221212", response)
        self.assertEqual(response.status_code, 301)

    def testsetup13(self):
        client = Client()
        response = client.get('/to_do_list')
        print("response content for testsetup 13131313133113", response)
        self.assertEqual(response.status_code, 301)

    def testsetup14(self):
        client = Client()
        response = client.get('/comment')
        print("response content for testsetup 14141414141414", response)
        self.assertEqual(response.status_code, 301)







    # class SupporterTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(
#             username='jacob', email='jacob@…', password='top_secret')
#         User.objects.create(user=User.objects.get(username='jacob'),email='email1@gmail.com' , skype_username='email1',   mobile_no='68468168')
#         # Supporter.objects.create(user=User(),email='email2@gmail.com' , skype_username='email2',   mobile_no='635465151')
#
#     def testsetup1(self):
#         pass
#         emailuser1=User.objects.all()
#         print("emailuser****************************",emailuser1)
#         print("emailuserr comment &&&&&&&&&&&&&&&&&&&&&&&&&",emailuser1.filter( skype_username='email1'))
#         # emailuser2=Supporter.objects.get(skype_username='email2')
#         self.assertContains(emailuser1.comment_set,'comment ')
#
#
#         self.assertEqual(emailuser2.comment_set.all(),'comment set so second test case passed')
#

# class ProjectTestCase(TestCase):
    # def setUp(self):
    #     self.factory = RequestFactory()
    #     Project.objects.create(project_description='first project')
    #     Project.objects.create(project_description='second project')

    # def testsetup2(self):
    #     client = Client()
    #     response = client.get('/add_project')
    #     print("response content **************",response.content)
        # print("response.contexttttttttttttttttttttttttt",response.context[''])
        # request = self.factory.get(project_description='movie booking app')
        # request.user = self.user
        # response = ProjectViewset.project_comment(request)
        # self.assertEqual(response.status_code, 301)

        # objectget1=Project.objects.get(project_description='first project')
        # print("objectget11111111111111111111111111111111",objectget1)
        # objectget2=Project.objects.get(project_description='second project')
        # self.assertAlmostEqual(objectget1.available_comments,'comment')
        # self.assertEqual(objectget2.completion_date,'available_comments 2')
    # def testsetup3(self):
    #     obj=Project.objects.create(project_description='second project')
    #     time=datetime.now()
    #     print("tiiiiiiiiiiiiiiiimmmmmmmmmmmmmmmmeeeeeeeeeeeeee",datetime.astimezone())
    #     self.assertEqual(obj.assigned_date,datetime.now())



