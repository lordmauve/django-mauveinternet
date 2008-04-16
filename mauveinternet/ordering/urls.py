from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$', 'mauveinternet.ordering.views.orders_new'),
	(r'^all$', 'mauveinternet.ordering.views.orders_all'),
	(r'^(?P<code>[0-9]+)/$', 'mauveinternet.ordering.views.view_order'),
)


