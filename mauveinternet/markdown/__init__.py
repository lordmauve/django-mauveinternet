from django import forms

class MarkdownTextarea(forms.Textarea):
	class Media:
		css = {'all': ['css/markdown/markdownarea.css']}
		js = ['js/lib/prototype.js', 'js/markdown/livepipe/livepipe.js', 'js/markdown/livepipe/textarea.js', 'js/markdown/showdown.js', 'js/markdown/markdownarea.js']

	def __init__(self, attrs={}):
		super(MarkdownTextarea, self).__init__(attrs)
		self.attrs.update({'class': 'markdown'})


_link_providers = set()

def register_linkable(model):
	_link_providers.add(model)

def get_models():
	"""Returns a list of linkable ('appname.Model', 'Verbose name') pairs"""
	return [('%s.%s' % (m._meta.app_label, m._meta.object_name), m._meta.verbose_name.capitalize()) for m in _link_providers]

def get_model(mname):
	"""Return a linkable model for the given 'appname.Model' string"""
	for m in _link_providers:
		if mname == ('%s.%s' % (m._meta.app_label, m._meta.object_name)):
			return m
	raise ValueError("No linkable model found matching '%s'" % mname)
