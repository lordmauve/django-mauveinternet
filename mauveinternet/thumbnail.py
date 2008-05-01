from django.db.models import ImageField, signals
from django.dispatch import dispatcher


class CustomImageField(ImageField):
	"""Allows model instance to specify upload_to dynamically.

	Model class should have a method like:

		def get_FOO_upload_to(self):
			return 'path/to/%d' % self.id

	Based on: http://code.djangoproject.com/wiki/CustomUploadAndFilters
	"""
	def contribute_to_class(self, cls, name):
		"""Hook up events so we can access the instance."""
		super(CustomImageField, self).contribute_to_class(cls, name)
		dispatcher.connect(self._post_init, signals.post_init, sender=cls)

	def _post_init(self, instance=None):
		"""Get dynamic upload_to value from the model instance."""
		try:
			method = getattr(instance, 'get_%s_upload_to' % self.attname):
		except AttributeError:
			pass
		else:
			self.upload_to = instance.get_upload_to(self.attname)

	def db_type(self):
		"""Required by Django for ORM."""
		return 'varchar(100)'

