from .models import Cart, CartItem


def cart_count(request):

    count = 0

    session_key = request.session.session_key

    if session_key:

        try:
            cart = Cart.objects.get(
                session_key=session_key
            )

            count = CartItem.objects.filter(
                cart=cart
            ).values_list(
                "quantity",
                flat=True
            )

            count = sum(count)

        except Cart.DoesNotExist:
            count = 0

    return {
        "cart_count": count
    }