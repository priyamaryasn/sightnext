from django.conf.urls import url
from .views import all_cat,all_blogs

urlpatterns=[
	url(r'^$', all_cat, name="all_cat"),
	url(r'^(?P<name>[\w]+)/$', all_blogs, name="all_blogs")
]