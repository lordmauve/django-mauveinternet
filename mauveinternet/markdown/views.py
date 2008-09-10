import re
from django.http import HttpResponse, Http404

from mauveinternet.markdown import _link_providers

def links(request):
	if 'model' not in request.GET:
		# output a JSON serialisation of the model list
		models = [{'app': m._meta.app_label, 'model': m._meta.object_name, 'verbose_name': m._meta.verbose_name.capitalize()} for m in _link_providers]
		return HttpResponse('LinkDialog.updateModels({%s});' % (u',\n'.join([u"'%(app)s.%(model)s': '%(verbose_name)s'" % m for m in models])).encode('utf8'), mimetype='application/javascript; charset=UTF-8')
	else:
		model = request.GET['model']
		for m in _link_providers:
			if model == ('%s.%s' % (m._meta.app_label, m._meta.object_name)):
				break
		else:
			raise Http404()

		links = [(i.pk, unicode(i)) for i in m._default_manager.all()]
		return HttpResponse('LinkDialog.updateInstances({%s})' %
			(u',\n'.join([u"%d: '%s'" % l for l in links])).encode('utf8'),
			mimetype='application/javascript; charset=UTF=8')
