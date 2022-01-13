from django import template
from books.models import OrderItem,Book

register = template.Library()

@register.filter
def req_item_count(user):
    if user.is_authenticated:
        
        books = Book.objects.filter(merchant=user)
        qs = OrderItem.objects.filter(item__in=books, ordered=True, mer=False)  

        if qs.exists():
            return qs.count()
    
    return 0