from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CheckoutForm
from .models import Order, OrderItem
from products.models import Cart, CartItem


@login_required
def checkout(request):

    if not request.session.session_key:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    try:
        cart = Cart.objects.get(
            session_key=request.session.session_key
        )

    except Cart.DoesNotExist:

        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    cart_items = CartItem.objects.select_related(
        "product"
    ).filter(cart=cart)

    if not cart_items.exists():

        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = Order.objects.create(

                user=request.user,

                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                pincode=form.cleaned_data["pincode"],

                total_amount=total,

            )

            for item in cart_items:

                OrderItem.objects.create(

                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,

                )

                item.product.stock -= item.quantity
                item.product.save()

            cart_items.delete()

            messages.success(
                request,
                "Your order has been placed successfully!"
            )

            return redirect("order_success")

    else:

        form = CheckoutForm(initial={
            "full_name": request.user.get_full_name(),
            "email": request.user.email,
        })

    return render(request, "orders/checkout.html", {

        "form": form,
        "cart_items": cart_items,
        "total": total,

    })
@login_required
def my_orders(request):

    return render(request, "orders/my_orders.html")


@login_required
def order_success(request):

    return render(request, "orders/order_success.html")