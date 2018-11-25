from django.conf.urls import include, url
from rest_framework import routers

from .views import AccountViewSet, NewAuthToken

router = routers.DefaultRouter()
router.register(r'users', AccountViewSet)


urlpatterns = [
    url(r'', include(router.urls)),
    url(r'auth/?$', NewAuthToken.as_view())
]
