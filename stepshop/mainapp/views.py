from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


def products(request, pk=None):
    title = "продукт | каталог"

    links_menu = ProductCategory.objects.all()
    products_all = Product.objects.all().order_by('price')

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'title': title,
        'links_menu': links_menu,
        'products_all': products_all,
        'basket': basket,
    }

    if pk is not None:
        if pk == 0:
            products_all = Product.objects.all().order_by('price')
            category = {'name': 'все'}

        elif pk == 1:
            products_all = Product.objects.all().filter(created_user__pk=request.user.pk).order_by('price')
            category = {'name': 'Ваши продукты'}

        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_all = Product.objects.filter(category__pk=pk).order_by('price')

        context['category'] = category
        context['products_all'] = products_all

    return render(request=request, template_name='mainapp/products.html', context=context)


def product(request, pk):
    title = "продукт"

    current_product = get_object_or_404(Product, pk=pk)
    name = current_product.created_user
    if request.user.is_authenticated:
        if current_product.created_user.pk == request.user.pk:
            name = 'Вы'
    products_all = Product.objects.filter(category__pk=current_product.category.pk).exclude(pk=current_product.pk).order_by('price')[:12]

    context = {
        'title': title,
        'current_product': current_product,
        'name': name,
        'products_all': products_all,
    }

    return render(request=request, template_name='mainapp/product.html', context=context)

def create_product(request):
    title = 'регистрация'

    if request.method == 'POST':
        print(request.POST)
        '''register_form = Product(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()'''

    context = {
        'title': title,
    }

    return render(request, 'mainapp/create_product.html', context)
