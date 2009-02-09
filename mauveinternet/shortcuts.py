import sys

from django.http import HttpResponse, HttpResponseForbidden
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


def forbidden(request):
        t = loader.get_template("forbidden.html")
        c = RequestContext(request)
        return HttpResponseForbidden(t.render(c), mimetype='text/html; charset=UTF-8')


import django.http

class HttpResponseRedirect(django.http.HttpResponseRedirect):
	"""A subclass of HttpResponseRedirect that can accept as the first argument
	either a string or any object with a method get_absolute_url"""
	def __init__(self, url_or_model, *args, **kwargs):
		if hasattr(url_or_model, 'get_absolute_url'):
			url = url_or_model.get_absolute_url()
		else:
			url = url_or_model

		super(HttpResponseRedirect, self).__init__(url, *args, **kwargs)

from django.core.urlresolvers import reverse

def redirect(name, *args, **kwargs):
	"""Looks up a view using URL reversing and then redirects to it"""
	url = reverse(name, args, kwargs)
	return HttpResponseRedirect(url)
