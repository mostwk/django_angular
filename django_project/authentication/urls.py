from django.conf.urls import url, include
from rest_framework import routers
from django_project.authentication import views
from rest_framework.authtoken.views import ObtainAuthToken


router = routers.DefaultRouter()
router.register(r'users', views.AccountViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'auth/', ObtainAuthToken.as_view())
]
