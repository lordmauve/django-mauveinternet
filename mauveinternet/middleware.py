class MessageWriter(object):
	def __init__(self, session):
		self.session=session
	
	def __call__(self, message):
		try:
			self.session['messages'].append(message)
		except KeyError:
			self.session['messages']=[message]

class MessageMiddleware(object):
	"""Guerilla patches request.user. to add a write_message function.

	The corresponding Request Context Processor is
	mauveinternet.context_processors.messages
	"""
	def process_request(self, request):
		request.user.write_message=MessageWriter(request.session)
		

class ContentTypeMiddleware(object):
	def process_response(self, request, response):
		try:
			if 'application/xhtml+xml' not in request.META['HTTP_ACCEPT'] and response['Content-Type'].startswith('application/xhtml+xml'):
				response['Content-Type']='text/html; charset=UTF-8'
		except KeyError:
			pass

		return response
