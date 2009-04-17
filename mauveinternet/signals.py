class Signal(object):
	"""Simple class providing event dispatch functionality; this is a
	minimal backport of Django 1.0's signal class.

	This allows us to define our own signals in a standardised way, but
	cannot be used to receive events emitted by pre-Django-1.0 model hooks.
	"""
	def __init__(self, providing_args=[]):
		self.callbacks = []

	def connect(self, callback):
		self.callbacks.append(callback)

	def send(self, sender, **kwargs):
		for c in self.callbacks:
			c(sender, **kwargs)		
