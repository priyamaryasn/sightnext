"""sight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
import Home.views
import Users.views
import followers.views
import Blogs.views
import FollowCategory.views
from django.contrib.auth.views import password_reset, password_reset_done,password_reset_confirm,password_reset_complete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cards/', include('Blogs.urls', namespace="cards")),
    url(r'^users/', include('Users.urls')),
    url(r'^comments/', include('Comments.urls')),
    url(r'^likes/', include('Likes.urls')),
    url(r'^journal/', include('journal.urls')),
    url(r'^categories/',include('categories.urls',namespace="category")),
    url(r'^subscribe/',include('FollowCategory.urls',namespace="FollowCategory")),
    # url(r'^copy/$',FollowCategory.views.checko),
    url(r'^$', Blogs.views.all_cards, name="home"),
    url(r'^about/$', Users.views.about, name="about"),
    url(r'^contact/$', Users.views.contact, name="contact"),
    url(r'^follow/(?P<username>\w+)/$', followers.views.follow, name="follow"),
    url(r'^froala_editor/', include('froala_editor.urls')),
    url(r'^user/password/reset/$',password_reset,name="password_reset"),
    url(r'^user/password/reset/done/$',password_reset_done, name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',password_reset_confirm, name="password_reset_confirm"),
    url(r'^user/password/done/$', password_reset_complete,name="password_reset_complete"),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
