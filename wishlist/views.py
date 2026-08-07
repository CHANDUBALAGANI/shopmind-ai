from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Wishlist
from products.models import Product


@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if created:

        messages.success(
            request,
            "Product added to your wishlist."
        )

    else:

        messages.info(
            request,
            "Product is already in your wishlist."
        )

    return redirect("product_list")


@login_required
def wishlist_view(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related("product")

    return render(
        request,
        "wishlist/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


@login_required
def remove_from_wishlist(request, wishlist_id):

    wishlist_item = get_object_or_404(
        Wishlist,
        id=wishlist_id,
        user=request.user
    )

    wishlist_item.delete()

    messages.success(
        request,
        "Product removed from wishlist."
    )

    return redirect("wishlist")


@login_required
def move_to_cart(request, wishlist_id):

    wishlist_item = get_object_or_404(

        Wishlist,

        id=wishlist_id,

        user=request.user

    )

    product = wishlist_item.product

    session_key = request.session.session_key

    if not session_key:

        request.session.create()

        session_key = request.session.session_key

    from products.models import Cart, CartItem

    cart, created = Cart.objects.get_or_create(

        session_key=session_key

    )

    cart_item, created = CartItem.objects.get_or_create(

        cart=cart,

        product=product

    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    wishlist_item.delete()

    messages.success(

        request,

        "Moved to cart successfully."

    )

    return redirect("wishlist")