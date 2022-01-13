from django import template
from books.models import OrderItem, Book

register = template.Library()


@register.filter
def rtn_item_count(user):
    count = 0
    if user.is_authenticated:        
        qs1 = OrderItem.objects.filter(ordered=True,return_started = True,returned = False, dagent=user)
        qs2 = OrderItem.objects.filter(ordered=True,return_started = True,returned = False, dagent=None)
        
        if qs1.exists():
            count += qs1.count()
        
        if qs2.exists():
            count += qs2.count()    

        return count   

    return 0