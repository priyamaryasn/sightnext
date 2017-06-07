from django.conf.urls import url
from .views import follow_cat

urlpatterns=[
	url(r'^sub/(?P<name>[\w]+)/$',follow_cat,name="follow_cat")
	]