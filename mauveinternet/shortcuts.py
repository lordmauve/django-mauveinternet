import sys

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext, loader, Context

def template(request, templ, **kwargs):
	"""Shortcut for creating a response using a template.
	This improves on django.shortcuts.render_to_response in several ways:

	* it's shorter to type
	* it uses the more succinct kwargs syntax to pass variables to templates
	* it always uses a RequestContext
	* if you pass a list of template names it selects the first one that exists

	"""
	if isinstance(templ, list) or isinstance(templ, tuple):
	        t = loader.select_template(templ)
	else:
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
	if not args:
		args = None

	if not kwargs:
		kwargs = None

	url = reverse(name, args, kwargs)
	return HttpResponseRedirect(url)


def updated(request, message, next=None, allow_continue=True):
	"""Redirects the user, with the message provided.

	This is a common action following views that have saved form data, hence the name updated() to
	reflect the notion of informing a user of the save.

	Additionally, this handles save versus save and continue editing. By default, redirects users
	back to the current URL, allowing them to continue editing. If the 'next' argument is
	provided, this URL is redirected to instead of the request URL, unless the form data contains
	a variable named 'continue'. For image buttons, this is handled in a way compatible with
	Internet Explorer.

	'allow_continue' disables this behaviour, forcing a redirect to 'next'.
	"""
	if hasattr(request.user, 'write_message'):
		request.user.write_message(message)
	else:
		request.user.message_set.create(message=message)

	if next and (not allow_continue or ('continue' not in request.POST and 'continue.x' not in request.POST)):
		return HttpResponseRedirect(next)
	return HttpResponseRedirect(request.path)
