import re
from django.http import HttpResponse, Http404

from mauveinternet.markdown import get_models, get_model

def links(request):
	if 'model' not in request.GET:
		# output a JSON serialisation of the model list
		return HttpResponse('LinkDialog.updateModels({%s});' % (u',\n'.join([u"'%s': '%s'" % (mname, vname.replace(u"'", u"\\'")) for mname, vname in get_models()])).encode('utf8'), mimetype='application/javascript; charset=UTF-8')
	else:
		try:
			model = get_model(request.GET['model'])
		except ValueError:
			raise Http404()

		links = [(i.pk, unicode(i)) for i in model._default_manager.all()]
		return HttpResponse('LinkDialog.updateInstances({%s})' %
			(u',\n'.join([u"%d: '%s'" % (pk, title.replace("'", "\\'")) for pk, title in links])).encode('utf8'),
			mimetype='application/javascript; charset=UTF=8')
