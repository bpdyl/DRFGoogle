"""DRFGoogle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,re_path,include
from Accounts.views import MyView,PostView, UpdateProfileView,home,my_profile,profile_update
from django.views.generic import TemplateView
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.conf import settings

router = DefaultRouter()
router.register('update_user_profile',UpdateProfileView,basename='update-user-profile')
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="index.html")),
    path('',home,name='home'),
    path('profile',my_profile,name='profile'),
    path('api-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    re_path('read/',MyView.as_view(), name='read'),
    re_path('post/',PostView.as_view({'get':'list','post':'create'}),name='post-action'),
    re_path('update_user_profile/',UpdateProfileView.as_view({'post':'update','get':'list','patch':'update'}),name='update-user-profile'),
    # re_path('',include(router.urls),name='update-user-profile'),
    path('profile-fill/',profile_update,name='profile-fill'),
    path('accounts/',include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)