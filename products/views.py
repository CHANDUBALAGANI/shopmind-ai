from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Cart, CartItem

def product_list(request):

    category_id = request.GET.get('category')
    search = request.GET.get('search')

    products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'products/product_detail.html', {
        'product': product
    })



def add_to_cart(request, product_id):

    # Create a session if it doesn't exist
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(
        session_key=session_key
    )

    # Get the selected product
    product = get_object_or_404(Product, id=product_id)

    # Check if product already exists in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # If it already existed, increase quantity
    if not created:

     if cart_item.quantity < product.stock:

          cart_item.quantity += 1
          cart_item.save()
    return redirect('product_list')



def cart_view(request):

    # If there is no session yet, show an empty cart
    if not request.session.session_key:
        return render(request, 'products/cart.html', {
            'cart_items': [],
            'total': 0,
        })

    session_key = request.session.session_key

    try:
        cart = Cart.objects.get(session_key=session_key)
        cart_items = CartItem.objects.filter(cart=cart)

    except Cart.DoesNotExist:
        cart_items = []

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })



def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    # Increase only if stock is available
    if cart_item.quantity < cart_item.product.stock:

        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

    else:

        cart_item.delete()

    return redirect('cart')



def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    cart_item.delete()

    return redirect('cart')