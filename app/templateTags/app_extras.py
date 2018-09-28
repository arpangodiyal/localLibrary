from django import template

register = template.Library()

@register.filter
def set(value):
	return 1