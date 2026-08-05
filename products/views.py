from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product, Category, Cart, CartItem


def product_list(request):

    category_id = request.GET.get('category')
    search = request.GET.get('search')
    sort = request.GET.get('sort')

    products = Product.objects.select_related('category').all()

    # Category Filter
    if category_id:
        products = products.filter(category_id=category_id)

    # Search
    if search:
        products = products.filter(name__icontains=search)

    # Sorting
    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "name":
        products = products.order_by("name")

    else:
        products = products.order_by("-created_at")

    # Pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
        'selected_sort': sort,
    })


def product_detail(request, pk):

    product = get_object_or_404(Product, pk=pk)

    return render(request, 'products/product_detail.html', {
        'product': product
    })


def add_to_cart(request, product_id):

    # Create session if it doesn't exist
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # Get or create cart
    cart, created = Cart.objects.get_or_create(
        session_key=session_key
    )

    # Selected product
    product = get_object_or_404(Product, id=product_id)

    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # Product already exists in cart
    if not created:

        if cart_item.quantity < product.stock:

            cart_item.quantity += 1
            cart_item.save()

            messages.success(
                request,
                f"{product.name} added to your cart."
            )

        else:

            messages.warning(
                request,
                f"Only {product.stock} items are available in stock."
            )

    else:

        messages.success(
            request,
            f"{product.name} added to your cart."
        )

    return redirect('product_list')


def cart_view(request):

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

    if cart_item.quantity < cart_item.product.stock:

        cart_item.quantity += 1
        cart_item.save()

        messages.success(
            request,
            f"{cart_item.product.name} quantity updated."
        )

    else:

        messages.warning(
            request,
            f"Only {cart_item.product.stock} items are available in stock."
        )

    return redirect('cart')


def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save()

        messages.info(
            request,
            "Quantity decreased."
        )

    else:

        cart_item.delete()

        messages.warning(
            request,
            "Product removed from cart."
        )

    return redirect('cart')


def remove_from_cart(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    product_name = cart_item.product.name

    cart_item.delete()

    messages.warning(
        request,
        f"{product_name} removed from your cart."
    )

    return redirect('cart')