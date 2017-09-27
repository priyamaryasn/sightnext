from django.conf.urls import url
from .views import create_journal,add_single,show_all


urlpatterns = [
	url(r'^createjournal/$',create_journal, name="create_journal"),
	url(r'^add/(?P<name>[\w-]+)/$', add_single,name="add_single"),
	url(r'^(?P<name>[\w-]+)/$', show_all,name="show_all"),
]