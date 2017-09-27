from django.conf.urls import url
from .views import write_comment

urlpatterns = [
	url(r'^comment/(?P<name>[\w+-]+)/$', write_comment, name='comment'),

]