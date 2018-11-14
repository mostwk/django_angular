from django.conf.urls import url, include
from rest_framework import routers
from django_project.authentication import views
from .views import NewAuthToken


router = routers.DefaultRouter()
router.register(r'', views.AccountViewSet)


urlpatterns = [
    url(r'users/?', include(router.urls)),
    url(r'auth/?$', NewAuthToken.as_view())
]
