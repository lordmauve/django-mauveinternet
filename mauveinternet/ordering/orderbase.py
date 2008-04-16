from django.conf import settings

__doc__ = """Defines common utilities for creating pluggable Order models."""

STATUS_OPTIONS=[
		('N', 'New'),
		('P', 'Paid'),
		('C', 'Completed'), # ie. paid and fulfilled
		('D', 'Declined'), # declined by payment gateway
		('F', 'Failed'),  # error from payment gateway
		('R', 'Rejected'), # manually rejected by user or administrator
	]

class OrderBase(object):
	def order_number(self):
		return '%05d'%(self.id+settings.ORDER_NUMBER_BASE)

	def set_status(self, status, message):
		self.orderstatuschange_set.create(previous_status=self.order_status, message=message)
		self.order_status=status
		self.save()

	def history(self):
		return self.orderstatuschange_set.order_by('date')

