from django import template

register = template.Library()

@register.filter
def lookup(dict,key):
	return dict[key]

@register.filter
def get_range(value): 
	return range(int(value))


@register.filter
def get_attribute(obj,name):
	return getattr(obj,name,u"")

	