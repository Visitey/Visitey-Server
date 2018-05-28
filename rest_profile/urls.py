"""rest_profile URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rest_profile.views import ProfileViewSet

# profile_list = ProfileViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# profile_detail = ProfileViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
#
# # API endpoints
#
# urlpatterns = format_suffix_patterns([
#     url('^profiles/$', profile_list, name='profile-list'),
#     url('^profiles/(?P<pk>[0-9]+)/$', profile_detail, name='profile-detail'),
# ])