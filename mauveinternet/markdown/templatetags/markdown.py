from django.conf import settings
from django.db.models.loading import get_model
from django import template
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

from mauveinternet.markdown import _link_providers

register = template.Library()

def lookup_link(internal_link):
	import re
	mo = re.match(r'internal:(?P<app_label>\w+)\.(?P<model_name>\w+)/(?P<pk>\d+)/?', internal_link)
	if not mo:
		raise ValueError('Malformed internal link')
	model = get_model(mo.group('app_label'), mo.group('model_name'))
	if model not in _link_providers:
		raise ValueError('Linking to %s is not permitted' % model._meta.verbose_name_plural)
	inst = model._default_manager.get(pk=mo.group('pk'))	
	return inst.get_absolute_url()
	

@register.filter
def markdown(value, arg=''):
	"""
	This version of the Markdown template filter is based on the version
	that is supplied with Django, but expands encoded internal links to
	the correct URLs.

	Another difference is that this version drops the heading level by two levels,
	which is useful  where <h1> is site title and <h2> is page title.

	Unlike Django's version of this function, we skip import/compatibility because
	a compatible version is bundled (this is at least Markdown 1.7, as
	earlier versions have bugs with Unicode support).
	"""
	import re
	from mauveinternet.markdown import markdown

	extensions = [e for e in arg.split(",") if e]
	if len(extensions) > 0 and extensions[0] == "safe":
		extensions = extensions[1:]
		safe_mode = True
	else:
		safe_mode = False
	html = markdown.markdown(force_unicode(value), extensions, safe_mode=safe_mode)
	html = re.sub(r'<(/?)h([12])(\s.*?)?>', lambda mo: '<%sh%d%s>' % (mo.group(1), min(6, int(mo.group(2))+2), mo.group(3) or ''), html)	
	html = re.sub(r'(<a\s+[^>]*)href="(internal:.*?)"', lambda mo: '%shref="%s"' % (mo.group(1), lookup_link(mo.group(2))), html) 
	return mark_safe(html)
markdown.is_safe = True
