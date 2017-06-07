from django.conf.urls import url
from .views import likes

urlpatterns = [
    url(r'^like/(?P<name>[\w]+)/$', likes, name='like'),
]
