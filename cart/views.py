from django.shortcuts import render
from .cart import Cart
from store.models import Product
from django.shortcuts import get_object_or_404
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart/cart-summary.html", {"cart": cart})


def cart_add(request):
    cart = Cart(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        try:
            product_id = int(request.POST.get("product_id"))
            product_quantity = int(request.POST.get("product_quantity"))
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product, product_qty=product_quantity)
            cart_quantity = cart.__len__()
            response = JsonResponse({"qty": cart_quantity})

            return response
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Cantidad o ID del producto no válidos."}, status=400
            )

    return JsonResponse(
        {
            "error": "Metodo "
            + request.method
            + " no permitido."
            + "Accion:"
            + str(request.POST.get("action"))
        },
        status=405,
    )


def cart_delete(request):
    cart = Cart(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        try:
            product_id = int(request.POST.get("product_id"))
            product = get_object_or_404(Product, id=product_id)
            cart.delete(product=product_id)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()

            response = JsonResponse({"qty": cart_quantity, "total": cart_total})
            return response

        except (ValueError, TypeError):
            return JsonResponse(
                {
                    "error": "No se pudo eliminar el producto "
                    + product.name
                    + " del carrito."
                },
                status=400,
            )

    return JsonResponse(
        {
            "error": "Metodo "
            + request.method
            + " no permitido."
            + "Accion:"
            + str(request.POST.get("action"))
        },
        status=405,
    )


def cart_update(request):
    cart = Cart(request)
    if request.method == "POST" and request.POST.get("action") == "post":
        try:
            product_id = int(request.POST.get("product_id"))
            product_quantity = int(request.POST.get("product_quantity"))

            cart.update(product=product_id, qty=product_quantity)
            cart_quantity = cart.__len__()
            cart_total = cart.get_total()
            response = JsonResponse({"qty": cart_quantity, "total": cart_total})

            return response
        except (ValueError, TypeError):
            return JsonResponse(
                {"error": "Cantidad o ID del producto no válidos."}, status=400
            )

    return JsonResponse(
        {
            "error": "Metodo "
            + request.method
            + " no permitido."
            + "Accion:"
            + str(request.POST.get("action"))
        },
        status=405,
    )
