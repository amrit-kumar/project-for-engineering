
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from consultant_app import views
from rest_framework import routers



router = DefaultRouter()
# router.register(r'check/', views.TokenTest,'abcd')
router.register(r'admin_panel', views.AdminPanelViewSet, 'abc')
router.register(r'add_consultant', views.AddConsultantViewSet, 'bcd')
router.register(r'add_supporter', views.AddSupporterViewSet, 'def')
router.register(r'supporter', views.SupporterDetailViewSet, 'def')

router.register(r'log', views.UserViewSet, 'def')



# router.register(r'consultant123',views.ConsultantViewset)
# router.register(r'consultant',views.ConsultantDetailViewset,base_name='Consultant')


urlpatterns = [
     url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('rest_auth.urls')),
    # url(r'^authenticate/', views.ConsultantViewset.as_view()),
]