from django.conf.urls import url, include
from rest_framework import routers
from django_project.blog import views


router = routers.DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)
router.register(r'posts/(?P<post_id>.+?)/comments', views.PostCommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
