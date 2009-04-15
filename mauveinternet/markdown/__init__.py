from util import MarkdownTextarea # for compatibility

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
