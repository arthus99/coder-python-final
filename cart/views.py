from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    return render(request, "cart/cart-summary.html")


def cart_add(request):
    cart = Cart(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        try:
            product_id = int(request.POST.get("product_id"))
            product_quantity = int(request.POST.get("product_quantity"))
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, product_qty=product_quantity)

            response = JsonResponse(
                {"Usted pidío:": product.title, " con un total de:": product_quantity}
            )

            return response
            # csrf: "{{csrf_token}}",
            # action: "post"
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Cantidad o ID del producto no válidos."}, status=400
            )

    return JsonResponse(
        {"error": "Metodo " + request.method + " no permitido."}, status=405
    )


def cart_delete(request): ...
def cart_update(request): ...
