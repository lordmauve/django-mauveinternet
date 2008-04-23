from django.db import models
from django.core.urlresolvers import reverse

class InlineHelp(models.Model):
	slug = models.SlugField()
	description = models.TextField(blank=True, help_text="This field may be formatted with Markdown.")

	def __unicode__(self):
		return self.slug

	def get_absolute_url(self):
		return reverse('quick-help', kwargs={'slug': self.slug})		

	class Admin:
		pass

	class Meta:
		verbose_name_plural = u'inline help'
