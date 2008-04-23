from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
      url(r'^ajax/(?P<slug>[\w-]+)$', 'findaholidaylet.help.views.ajax_help', name='ajax-help'),
      url(r'^quick/(?P<slug>[\w-]+)$', 'findaholidaylet.help.views.quick_help', name='quick-help'),
)

