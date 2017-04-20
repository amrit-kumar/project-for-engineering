"""consultad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from rest_framework import routers
from django.contrib import admin
from consultant_app.views import *
from django.conf.urls.static import static
from rest_framework.authtoken import views
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse



router=routers.DefaultRouter()
# router.register(r'admin_panel', AdminPanelViewSet, 'admin_panel')
router.register(r'supporter_panel', SupporterPanelViewSet, 'supporter_panel')
router.register(r'add_consultant', AddConsultantViewSet, 'consultant')
router.register(r'add_supporter', AddSupporterViewSet, 'support')
router.register(r'add_project', AddProjectViewSet, 'project')
router.register(r'supporter', SupporterDetailViewset, 'supporter')
router.register(r'logout', LogoutViewSet, 'logout')
router.register(r'register', RegisterViewSet, 'register')
router.register(r'log', UserViewSet, 'log')
router.register(r'active', GetActiveViewSet, 'active')
router.register(r'notification', NotificationViewSet, 'notification')
router.register(r'technology', TechnologyViewSet, 'technology')
router.register(r'to_do_list', To_do_listViewSet, 'to_do_list')
router.register(r'comment', CommentViewSet, 'comment')
router.register(r'global_search', GlobalSearchViewset, 'global_search')




urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    # url(r'^rest-auth/login/$', LoginViewCustom.as_view(), name='rest_login'),

    url(r'^accounts/', include('rest_auth.urls')),
    url(r'^rest_auth/registration/', include('rest_auth.registration.urls')),

    url(r'all_auth/', include('allauth.urls')),
    url(r'^', include('django.contrib.auth.urls')),

              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

