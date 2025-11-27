from django import template
from workload.models import Projet

register = template.Library() 

@register.filter
def get_class_name(value):
    return value.__class__.__name__

@register.filter
def get_status_display(code):
    """Retourne le label lisible d'un status de projet"""
    try:
        return Projet.Status(code).label
    except:
        return code

@register.filter
def pourcent(valeur, total):
    try:
        return round((valeur / total) * 100, 0) if total else 0
    except (ZeroDivisionError, TypeError):
        return 0

@register.filter(name='has_group') 
def has_group(user, group_name):
	return user.groups.filter(name=group_name).exists()

@register.filter
def model_name(obj):
    return obj.__class__.__name__

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''