import re
from datetime import timedelta

from django import forms
if hasattr(forms, 'Manipulator'):
	try:
		from django import newforms as forms
	except ImportError:
		from django import forms


class TimeField(forms.RegexField):
	"""A time field that works around the fact that Python times only represent
	a one-day range by representing times as (hour, minute) pairs.

	We could use timedeltas but seconds are very fiddly for many user-facing
	applications; converting to timedeltas is not hard.

	timedeltas can be used for the initial keyword argument, however."""

	TIME_REGEX=r'([0-9]+):([0-9]{2})'
	def __init__(self, *args, **kwargs):
		ka = {'regex': self.TIME_REGEX, 'initial': ':00'}
		ka.update(kwargs)

		initial = ka['initial']
		if isinstance(initial, timedelta):
			hours = initial.days * 24 + initial.seconds//3600
			minutes = ((initial.seconds % 3600) + 30) // 60
			if minutes > 59:
				hours = hours + 1
				minutes = 0
			ka['initial'] = '%d:%02d'%(hours, minutes)
			
		super(TimeField, self).__init__(*args, **ka)
	
	def clean(self, value):
		time = value
		mo = re.match(self.TIME_REGEX, time)
		if not mo:
			raise forms.ValidationError('Please enter a time in H:MM format')
		hour = int(mo.group(1))
		minute = int(mo.group(2))

		hour = hour + minute//60
		minute = minute % 60
		return hour, minute

