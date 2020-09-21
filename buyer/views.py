from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Item, Cart_Item, Cart, Payment_Info
from django.urls import reverse
from django.conf import settings
import stripe
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    all_items = Item.objects.all()
    cart = Cart.objects.filter(user = request.user, complete=False)
    if cart:       
        context = {'seller_item_list' : all_items, 'cart':cart[0]}
    else:
        context = {'seller_item_list' : all_items}

    return render(request, 'home.html', context)

@login_required
def addItemView(request, item_id):
    cart = Cart.objects.filter(user = request.user, complete = False)
    item = get_object_or_404(Item, id=item_id)
    cart_item = Cart_Item.objects.create(item_text=item.item_text, price=item.price, quantity=1)
    if cart:
        cart = cart[0]
    else:
        cart = Cart.objects.create(user = request.user, total=0, tax=0, total_after_tax=0)
    
    find_item = cart.cart_items.filter(item_text = item.item_text)

    if find_item:
        find_item[0].quantity += 1
        find_item[0].save()
    else:
        cart.cart_items.add(cart_item)


    return redirect(reverse('home',))

@login_required
def removeItemView(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    item.delete()

    return redirect(reverse('home',))

@login_required
def checkoutView(request):
    check_cart = Cart.objects.filter(user = request.user, complete=False)
    if not check_cart:
        return redirect(reverse('home',))


    cart = Cart.objects.get(user = request.user, complete=False)
    
    if cart.complete == True:
        print("hello")
    stripe.api_key = "sk_test_51HTYDxD0aU2nDPoO9gmNsLyiv4YPrIEPB8qYeUPBEONnMWEcRlMescXJ7Ejl2CVSRHMtWabVYsTOuNyVrbSZoarH00HHmsNUEB"
    session = stripe.checkout.Session.create(
        success_url=request.build_absolute_uri(reverse('home')),
        cancel_url=request.build_absolute_uri(reverse('home')),
        payment_method_types=["card"],
        line_items=[
            {
                'price_data': {
                    'currency': 'cad',
                    'unit_amount': int(cart.total_price() * 100),
                    'product_data': {
                        'name': 'checkout_items'
                    }

                },
                'quantity': 1,
            },
        ],
        mode="payment",
)
    print("people")
    cart.complete = True
    cart.save()

    payment_info = Payment_Info.objects.create(price= cart.total_price(), user=request.user, stripe_id=session.payment_intent)
    payment_info.save()

    
    context = {'cart':cart, 'session_id': session.id,
     'stripe_public_key': settings. STRIPE_PUBLIC_KEY}
    return render(request, 'checkout.html', context)