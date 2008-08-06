import re

from django.conf import settings
from django.http import Http404
from django.views.static import serve


def assets(request, path):
        """Static file service.

	Wraps django.views.static.serve in such a way that for Internet Explorer 6,
	files in /ie6assets/, where available, will be served in place of files in /assets/.

	This is typically used to serve non-transparent (precomposited) versions of transparent
	.PNG images.
	"""

        ua = request.META.get('HTTP_USER_AGENT', '')
	resp = None
        if re.search(r'MSIE [3-6]', ua) and 'Opera' not in ua:
                try:
                        resp = serve(request, path=path, document_root=settings.MEDIA_ROOT.replace('assets', 'ie6assets'))
                except Http404:
                        pass

	if not resp:
	        resp = serve(request, path=path, document_root=settings.MEDIA_ROOT)
	
	vary = [hdr.strip() for hdr in resp.get('Vary', '').split(',')]
	resp['Vary'] = ', '.join(['User-Agent'] + vary)

	return resp
