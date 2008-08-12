from django import forms

class MarkdownTextarea(forms.Textarea):
	class Media:
		css = {'all': ['css/markdown/markdownarea.css']}
		js = ['js/lib/prototype.js', 'js/markdown/livepipe/livepipe.js', 'js/markdown/livepipe/textarea.js', 'js/markdown/showdown.js', 'js/markdown/markdownarea.js']

	def __init__(self, attrs={}):
		super(MarkdownTextarea, self).__init__(attrs)
		self.attrs.update({'class': 'markdown'})

