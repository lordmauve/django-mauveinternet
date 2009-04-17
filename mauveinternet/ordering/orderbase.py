"""Defines common utilities for creating pluggable Order models."""

from django.conf import settings

try:
	from django.dispatch import Signal
except ImportError:
	from mauveinternet.signals import Signal


# base set of order status options;
# these are expected to be present for payment handlers to use

STATUS_OPTIONS=[
		('N', 'New'),
		('P', 'Paid'),
		('C', 'Completed'), # ie. paid and fulfilled
		('D', 'Declined'), # declined by payment gateway
		('F', 'Failed'),  # error from payment gateway
		('R', 'Rejected'), # manually rejected by user or administrator
	]


class OrderBase(object):
	"""Mix-in class providing some additional methods for order implementations"""

	# Signal so that apps can opt to receive order status change events
	status_change = Signal(providing_args=['status', 'previous_status'])

	def order_number(self):
		return '%05d' % (self.id + settings.ORDER_NUMBER_BASE)

	def get_total(self):
		return self.total

	def set_status(self, status, message):
		prevstatus = self.status
		self.orderstatuschange_set.create(previous_status=prevstatus, message=message)
		self.status = status
		self.save()

		# Dispatch signal
		self.status_change.send(sender=self, status=status, previous_status=prevstatus)

	def history(self):
		return self.orderstatuschange_set.order_by('date')

