from .models import Cart


def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.total_items
        except Cart.DoesNotExist:
            count = 0
    else:
        if request.session.session_key:
            try:
                cart = Cart.objects.get(session_key=request.session.session_key)
                count = cart.total_items
            except Cart.DoesNotExist:
                count = 0
        else:
            count = 0
    
    return {'cart_count': count}