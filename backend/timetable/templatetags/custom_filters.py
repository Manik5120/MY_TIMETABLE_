from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Template filter to get an item from a dictionary using a key.
    Usage: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    try:
        # Try to get the value using the key as is
        value = dictionary.get(key)
        if value is not None:
            return value
        
        # Try converting to integer if it's a string
        if isinstance(key, str) and key.isdigit():
            return dictionary.get(int(key))
        
        # Try converting to string if it's an integer
        if isinstance(key, int):
            return dictionary.get(str(key))
            
        return None
    except (ValueError, TypeError, AttributeError):
        return None

@register.filter(name='multiply')
def multiply(value, arg):
    """
    Multiplies the value by the argument
    Usage: {{ value|multiply:arg }}
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0 