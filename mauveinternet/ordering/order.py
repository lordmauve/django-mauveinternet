from decimal import Decimal, ROUND_CEILING

from django.conf import settings

class ItemNotRepeatable(Exception):
	"""Indicates that an attempt to add an item to the basket failed because
	it is already present and the item may not be added twice."""


class OrderItem(object):
	def __init__(self, name):
		self.name=name
		self.quantity=1

	def __eq__(self, i):
		"""Naive default implementation"""
		return self.__class__ == i.__class__ and self.name == i.name

	def __unicode__(self):
		return self.name

	def get_unit_price(self):
		raise NotImplementedError("OrderItem subclasses must define this method to return a Decimal value")

	def get_total_price(self):
		return self.quantity*self.get_unit_price()


class StackableOrderItem(OrderItem):
	def __init__(self, quantity=1, *args, **kwargs):
		OrderItem.__init__(self, *args, **kwargs)
		self.set_quantity(quantity)

	def set_quantity(self, quantity):
		self.quantity=quantity


class RepeatableOrderItem(OrderItem):
	"""Repeatable order items may be added multiple times to the basket."""

	def __eq__(self):
		return False


class BasketCharge(object):
	def get_charge(self, subtotal, orderitemlist):
		"""Subclasses must define this method to return a Decimal value:
		- positive for additional charges like VAT or Delivery
		- negative for discounts

		Subtotal is provided for convenience, orderitemlist for completeness.
		"""

		raise NotImplementedError, "BasketCharge subclasses must define get_charge to return their charge or discount value"

	def __unicode__(self):
		raise NotImplementedError, "BasketCharge subclasses must define __unicode__ to return the name of the charge for display"


class VATCharge(object):
	"""Computes VAT for a basket whose items exclude VAT."""
	def get_charge(self, subtotal, orderitemlist):
		return (subtotal*Decimal('0.175')).quantize(Decimal('0.01'), ROUND_CEILING)

	def __unicode__(self):
		return u"VAT"


class DeliveryCharge(object):
	"""Applies a fixed delivery charge from settings"""
	def __init__(self):
		"""Store this in case it is changed later"""
		self.rate=settings.DELIVERY_CHARGE

	def get_charge(self, subtotal, orderitemlist):
		return self.rate

	def __unicode__(self):
		return u"Delivery"


class OrderItemList(object):
	def __init__(self):
		self.items=[]
		self.next_id=1	#incrementing id so we can uniquely identify items
		self.charges=[]

	def add(self, item):
		for i in self.items:
			if i == item:
				if hasattr(i, 'set_quantity'):
					i.set_quantity(i.quantity+item.quantity)
					return
				elif isinstance(i, RepeatableOrderItem):
					self.__append_item(item)
					return
				raise ItemNotRepeatable("You may only purchase a single instance of this item")

		self.__append_item(item)

	def __append_item(self, item):
		self.items.append(item)
		item.list_id=self.next_id
		self.next_id+=1

	def __iter__(self):
		for i in self.items:
			yield i

	def get_subtotal(self):
		return sum([i.get_total_price() for i in self.items])

	def get_charges(self):
		"""Build a list of charges for display.

		Returns a list of tuples (charge, value) where charge is a unicode string
		and value is a Decimal."""

		subtotal=self.get_subtotal()
		return [i for i in [(unicode(c), c.get_charge(subtotal, self)) for c in self.charges] if i[1]]

	def get_total(self):
		subtotal=self.get_subtotal()
		return subtotal+sum([c.get_charge(subtotal, self) for c in self.charges])

	def get_item(self, id):
		for item in self.items:
			if item.list_id == id:
				return item
		raise KeyError("No item with this ID was found in the basket.")

	def remove_item(self, id):
		for i, item in enumerate(self.items):
			if item.list_id == id:
				self.items=self.items[:i]+self.items[i+1:]
				return item
		raise KeyError("No item with this ID was found in the basket.")

	def is_empty(self):
		return len(self.items) == 0

	def fulfil(self):
		for i in self.items:
			if hasattr(i, 'fulfil'):
				i.fulfil()
