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
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from consultant_app import views
from rest_framework import routers



router = DefaultRouter()
# router.register(r'check/', views.TokenTest,'abcd')
router.register(r'checks', views.AdminPanelViewSet)
router.register(r'consultant',views.ConsultantViewset)



urlpatterns = [
     url(r'^', include(router.urls)),
    # url(r'^check/', views.ConsultantViewset.as_view() ),
    # url(r'^check/', views.TokenTest.as_view(),name='checking'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('rest_auth.urls')),
    # url(r'^authenticate/', views.ConsultantViewset.as_view()),

]