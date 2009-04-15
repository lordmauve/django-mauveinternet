from django.db.models import TextField
from django.contrib.admin import ModelAdmin
from django import forms

class MarkdownTextField(TextField):
	"""This class does nothing different as the current implementation
	of Django's ModelAdmin would override any custom .formfield() method.
	Instead this just flags a textfield as being formatted in Markdown
	syntax."""


class MarkdownTextarea(forms.Textarea):
	"""A textarea widget that adds Javascript toolbars and previews for editing
	Markdown code"""
	class Media:
		css = {'all': ['css/markdown/markdownarea.css']}
		js = ['js/lib/prototype.js', 'js/markdown/livepipe/livepipe.js', 'js/markdown/livepipe/textarea.js', 'js/markdown/showdown.js', 'js/markdown/markdownarea.js']

	def __init__(self, attrs={}):
		super(MarkdownTextarea, self).__init__(attrs)
		self.attrs.update({'class': 'markdown'})


class MarkdownModelAdmin(ModelAdmin):
	"""A modeladmin that detects MarkdownTextFields and replaces the
	admin widget with a MarkdownTextArea."""
	def formfield_for_dbfield(self, dbfield, **kwargs):
		if isinstance(dbfield, MarkdownTextField):
			return forms.CharField(widget=MarkdownTextarea)
		return super(MarkdownModelAdmin, self).formfield_for_dbfield(dbfield, **kwargs)
