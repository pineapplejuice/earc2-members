from django import template

register = template.Library()

@register.filter(name='phone_number')
def phone_number(number):
	"""Convert 10 character string into (xxx) xxx-xxxx."""
	first = str(number[0:3])
	second = str(number[3:6])
	third = str(number[6:10])
	return '(' + first + ') ' + second + '-' + third
