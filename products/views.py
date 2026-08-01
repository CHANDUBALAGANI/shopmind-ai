from django.shortcuts import render, get_object_or_404
from .models import Product, Category


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