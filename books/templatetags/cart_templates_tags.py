from django import template
from books.models import Order, Review, Book
from django.shortcuts import render,redirect,get_object_or_404

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0