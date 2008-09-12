from django.contrib import admin
from mauveinternet.markdown import MarkdownTextarea

from models import *

class InlineHelpAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'has_description']
	
	def formfield_for_dbfield(self, db_field, **kwargs):
		if db_field.name == 'description':
			return db_field.formfield(widget=MarkdownTextarea, **kwargs)
		return super(InlineHelpAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(InlineHelp, InlineHelpAdmin)
