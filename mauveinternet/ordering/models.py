from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

from mauveinternet.ordering.picklefield import PickleField

from mauveinternet.ordering.order import OrderItemList
from mauveinternet.ordering.lockbox import Lockable

# Create your models here.
STATUS_OPTIONS=[
		('N', 'New'),
		('P', 'Paid'),
		('C', 'Completed'), # ie. paid and fulfilled
		('D', 'Declined'), # declined by payment gateway
		('F', 'Failed'),  # error from payment gateway
		('R', 'Rejected'), # manually rejected by user or administrator
	]

class Order(models.Model):
	order_status=models.CharField(max_length=1, choices=STATUS_OPTIONS, default='N')
	
	customer = models.ForeignKey(User)
	date_placed=models.DateTimeField(auto_now_add=True)

	vat_number = models.CharField(max_length=24, blank=True)

	billing_address=models.TextField()
	billing_postcode=models.CharField('Postcode', max_length=10)

	items=PickleField(OrderItemList)

	total=models.DecimalField(editable=False, max_digits=10, decimal_places=2)

	def order_number(self):
		return '%05d'%(self.id+settings.ORDER_NUMBER_BASE)

	def set_status(self, status, message):
		self.orderstatuschange_set.create(previous_status=self.order_status, message=message)
		self.order_status=status
		self.save()

	def history(self):
		return self.orderstatuschange_set.order_by('date')

	class Meta:
		permissions = [('can_view_orders', 'Permission to view orders')]

class OrderStatusChange(models.Model):
	order=models.ForeignKey(Order)
	date=models.DateTimeField(auto_now_add=True)
	previous_status=models.CharField(max_length=1, choices=STATUS_OPTIONS+[('-', '-')])
	message=models.CharField(max_length=255)

	def new_status(self):
		try:
			return self.order.orderstatuschange_set.filter(date__gt=self.date).order_by('date')[0].previous_status
		except IndexError:
			return self.order.order_status

	def get_new_status_display(self):
		s=self.new_status()
		disps=dict(STATUS_OPTIONS+[('-', '-')])
		return disps[s]
