
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_auth.registration.views import LoginViewC
from consultant_app import views
from allauth.account.views import confirm_email as allauthemailconfirmation
from rest_framework import routers


router = DefaultRouter()
router.register(r'admin_panel', views.AdminPanelHomePageViewSet, 'admin_panel')
router.register(r'add_consultant', views.AddConsultantViewSet, 'add_consultant')
router.register(r'add_supporter', views.AddSupporterViewSet, 'add_supporter')
router.register(r'supporter', views.SupporterDetailViewSet, 'supporter')

router.register(r'add_project', views.AddProjectViewSet, 'AddProjectViewSet')
router.register(r'register/supporter', views.SupporterRegisterViewSet, 'register_supporter')
router.register(r'activate_users', views.ActivateUser, 'activate_users')

router.register(r'accounts/profile', views.UserViewSet, 'after_emailverify_view')
router.register(r'project_delete', views.ProjectViewSet, 'project_delete')

router.register(r'to_do_list', views.ToDoListViewset, 'to_do_list')
router.register(r'notification', views.NotificationViewset, 'notification')

router.register(r'userregister', views.RegisterViewSet, 'userregister')

router.register(r'TechnologyViewset', views.TechnologyViewset, 'TechnologyViewset')
router.register(r'CommentViewset', views.CommentViewset, 'CommentViewset')




urlpatterns = [
     url(r'^', include(router.urls)),
    # url(r'^accounts/registration/',views.RegisterViewSet,name='custom_register'),
    # url(r'^accounts/registration/consulta', include('rest_auth.registration.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/logout/', views.LogoutViewSet),
    # url(r'^accounts/registration/account-confirm-email/(?P<key>\w+)/$', allauthemailconfirmation,
    #     name="account_confirm_email"),

    url(r'^accounts/', include('rest_auth.urls')),
    url(r'^accounts/registration/', include('rest_auth.registration.urls')),

    # url(r'^accounts/', include('allauth.urls')),
    url(r'^', include('django.contrib.auth.urls')),

    # url(r'^check/', views.TokenTest.as_view(),name='checking'),


]
