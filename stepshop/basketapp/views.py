from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def basket(request):
    if request.user.is_authenticated:
        user_basket = Basket.objects.filter(user=request.user)
        context = {
            'basket': user_basket
        }
        return render(request, 'basketapp/basket.html', context)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    if product.quantity > basket.quantity:
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity -= 1

    if basket.quantity <= 0:
        basket.delete()
    else:
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if basket:
        basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
