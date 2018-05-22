"""visitey URL Configuration

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
from allauth.account.views import confirm_email as allauthemailconfirmation
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import refresh_jwt_token

from rest_friendship.views import FriendshipViewSet, FriendshipRequestViewSet, FollowViewSet
from rest_profile.views import ProfileViewSet

# DOC VIEW
schema_view = get_schema_view(
    openapi.Info(
        title="visitey API",
        default_version='v1',
        description="Api for visitey server",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@visitey.fr"),
        license=openapi.License(name="BSD License"),
    ),
    # validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Routers provide an easy way of automatically determining the URL conf.
router = DefaultRouter()
router.register(r'profile', ProfileViewSet)
router.register(r'friendship', FriendshipViewSet, base_name='friend')
router.register(r'friendshiprequest', FriendshipRequestViewSet, base_name='friendshiprequest')
router.register(r'follow', FollowViewSet, base_name='follow')
# router.register(r'threads', ThreadView)
# router.register(r'messages', MessageView, 'messages')
# router.register(r'notifications', NotificationCheckView, 'notifications')
# router.register(r'authentication', ParticipantAuthenticationView, 'authentication')

urlpatterns = [
    url(r'^', include('rest_auth.urls')),
    url(r'^social/', include('rest_social.urls')),
    url(r'^registration/account-confirm-email/(?P<key>\w+)/$', allauthemailconfirmation, name="account_confirm_email"),
    url(r'^registration/', include('rest_auth.registration.urls')),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', schema_view.with_ui('swagger', cache_timeout=None), name="schema-swagger-ui"),
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]

# urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
