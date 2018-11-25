"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

from . import views

schema_view = get_swagger_view(title='SN API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(), name='index'),
    path(r'api/', include('django_project.authentication.urls')),
    path(r'api/', include('django_project.blog.urls')),
    path(r'docs/', schema_view)
]
