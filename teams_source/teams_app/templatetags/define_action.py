from django import template
register = template.Library()

@register.simple_tag
def get_primary(production:bool):
    if production:
        return "rr-dev-primary"
    else:
        return "rr-primary"
    
@register.simple_tag
def get_secondary(production:bool):
    if production:
        return "rr-dev-secondary"
    else:
        return "rr-secondary"