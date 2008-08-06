from django.contrib import admin
from models import *

class InlineHelpAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'has_description']

admin.site.register(InlineHelp, InlineHelpAdmin)
