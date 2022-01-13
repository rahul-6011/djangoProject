from django.shortcuts import render,redirect,get_object_or_404
from .models import Book,Order,OrderItem, Payment, Wishlist, Review
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import CheckoutForm
from django.views.generic import View
from django.conf import settings
import stripe
from deliveryagent.views import home_d

stripe.api_key = "settings.STRIPE_SECRET_KEY"


# Create your views here.

def home(request):

    all_books = Book.objects.all()

    if request.user.is_authenticated:
        
        acct = request.user.last_name
        
        if acct == 'merchant':
            return render(request,'home_m.html')

        elif acct == 'deliveryagent':
            return home_d(request)

        else:
            try:
                query1 = request.GET["search_book"]
                query2 = request.GET["search_author"]
                    
                if query1 or query2:
                    all_books = all_books.filter(name__contains = query1,author__contains = query2)

            finally:
                paginator = Paginator(all_books, 12 ) 
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request,'home.html',{'page_obj': page_obj})

    else :
        try:
            query1 = request.GET["search_book"]
            query2 = request.GET["search_author"]
                
            if query1 or query2:
                all_books = all_books.filter(name__contains = query1,author__contains = query2)

        finally:
            paginator = Paginator(all_books, 12 ) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request,'home.html',{'page_obj': page_obj})
        

@login_required
def cart(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)

    if order_items:
        order = Order.objects.filter(user = request.user, ordered=False)[0]
        return render(request,'cart.html',{'order_items':order_items , 'order':order})
    else:
        return render(request,'cart.html')

@login_required
def add_to_cart(request, id):
    print("add to cart")
    item = get_object_or_404(Book, id=id)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('home')
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('home')
    else:
        start_date = timezone.now()
        order = Order.objects.create(
            user=request.user, start_date=start_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('home')

@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(Book, id=id)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order_item.delete()
            return redirect('cart')
        
        else:
            return redirect('cart')
    
    else:
        return redirect('cart')

@login_required
def quantity_minus(request, id):
    item = get_object_or_404(Book, id=id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            return redirect("cart")
        else:
            return redirect("cart")
    else:
        return redirect("cart")

@login_required
def quantity_plus(request, id):
    item = get_object_or_404(Book, id=id)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect('cart')
        else:
            order.items.add(order_item)
            return redirect('cart')


class CheckoutView(View):
    def get(self, *args, **kwargs):
        order_items = OrderItem.objects.filter(user=self.request.user, ordered=False)
        order = Order.objects.filter(user = self.request.user, ordered=False)[0]
        form = CheckoutForm()
        context = {
            'form' : form,
            'order_items' : order_items,
            'order' : order
        }
        return render(self.request , 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            order_items = OrderItem.objects.filter(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')

                order.street_address = street_address
                order.apartment_address = apartment_address
                order.country = country
                order.zip = zip
                
                ordered_date = timezone.now()
                order.ordered_date = ordered_date
                order.save()
                if payment_option == 'CD':
                    return redirect('payment',payment_option = "card")
                elif payment_option == 'C':
                    for it in order_items:
                        it.ordered = True
                        it.save()
                    order.ordered = True
                    amount = int(order.get_total_price())
                    payment = Payment()
                    payment.stripe_charge_id = 'Cash'
                    payment.user = self.request.user
                    payment.amount = amount
                    payment.save()
                    order.payment = payment
                    order.save()
                    messages.success(self.request, "Order placed")
                    return redirect('home')
                else:
                    messages.warning(self.request, "Invalid Payment option")
                    return redirect("home")
            else:
                messages.warning(self.request, "Invalid Form")
                return redirect("home")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("home")

                
class PaymentView(View):
    def get(self, *args, **kwargs):
        order_items = OrderItem.objects.filter(user=self.request.user, ordered=False)
        order = Order.objects.filter(user = self.request.user, ordered=False)[0]
        context = {
            'order_items' : order_items,
            'order' : order
        }
        return render(self.request,"payment.html",context)

    def post(self, *args, **kwargs):
        token = self.request.POST.get('stripeToken')
        order = Order.objects.get(user = self.request.user, ordered=False)
        amount = int(order.get_total_price())

        try:
            stripe.Charge.create(
                amount=amount,
                currency="inr",
                source=token
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            order.ordered = True
            order.payment = payment
            ordered_date = timezone.now()
            order.ordered_date = ordered_date
            order.save()
            messages.success(self.request,"Your order was successful")
            return redirect('home')

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("home")

        except stripe.error.RateLimitError as e:
            messages.warning(self.request, "Rate Limit Error")
            return redirect("home")

        except stripe.error.InvalidRequestError as e:
            messages.warning(self.request, "Invalid Request Error")
            return redirect("home")
            
        except stripe.error.AuthenticationError as e:
           messages.warning(self.request, "Authentication Error")
           return redirect("home")

        except stripe.error.APIConnectionError as e:
           messages.warning(self.request, "API Connection Error")
           return redirect("home")

        except stripe.error.StripeError as e:
            messages.warning(self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("home")

        except Exception as e:
            messages.warning(self.request, "A serious error has been occurred. We have been notified.")
            return redirect("home")

@login_required
def wishlist(request):

    fav_books = Wishlist.objects.filter(user=request.user)

    if fav_books:
        paginator = Paginator(fav_books, 12 ) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'wishlist.html',{'page_obj': page_obj})
    else:
        return render(request,'wishlist.html')

@login_required
def add_to_wishlist_cart(request, id):
    print("add to cart")
    item = get_object_or_404(Book, id=id)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('wishlist')
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect('wishlist')
    else:
        start_date = timezone.now()
        order = Order.objects.create(
            user=request.user, start_date=start_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('wishlist')


@login_required
def add_to_wishlist(request, id):

    book = get_object_or_404(Book, id=id)

    fav_book, created = Wishlist.objects.get_or_create(user=request.user, book=book)

    if created:
        fav_book.save()
        messages.info(request, "Book added to wishlist")
        return redirect('home')
    else:
        messages.info(request, "Book already in wishlist")
        return redirect('home')

@login_required
def remove_from_wishlist(request, id):

    fav_book = get_object_or_404(Wishlist, id=id)

    if fav_book:
        fav_book.delete()
        messages.info(request, "Removed from wishlist")

    return redirect('wishlist')

def review(request, id):

    item = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        try:
            query = request.POST["drop_review"]
                
            if query:
                print(query)
                rev = Review.objects.create(customer=request.user, book=item, descrp=query)
                rev.save()

        finally:
            all_reviews = Review.objects.filter(book=item)
            return render(request,'review.html',{'all_reviews': all_reviews, 'book':item})

    else :    
        all_reviews = Review.objects.filter(book=item)
        return render(request,'review.html',{'all_reviews': all_reviews, 'book':item})