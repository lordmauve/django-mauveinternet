import sys

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader, Context

def template(request, templ, **kwargs):
        t = loader.get_template(templ)
        c = RequestContext(request, kwargs)
        return HttpResponse(t.render(c), mimetype='text/html; charset=UTF-8')

def MAGICTEMPLATE(templ):
	"""Experimental voodoo.

	Introspects the stack to discover the locals from the calling function,
	then renders the template using those locals.

	Could be used to simplify views that just unpack variables into the local
	scope then pass them to the template.

	The name of this function is in capitals to look like a macro.
 
	"""
	locals = sys._getframe(1).f_locals

        t = loader.get_template(templ)
        c = RequestContext(locals['request'], locals)
        return HttpResponse(t.render(c), mimetype='text/html; charset=UTF-8')
