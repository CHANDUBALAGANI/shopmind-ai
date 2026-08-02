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
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product_list')