def messages(request):
	variables={}

	if 'messages' in request.session:
		variables['messages']=request.session['messages']
		del(request.session['messages'])

	return variables

