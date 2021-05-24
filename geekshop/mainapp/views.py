from random import sample
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return sample(list(products), 1)[0]


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]
    return same_products


def products(request, pk=None, page=1):
    title = 'продукты'
    category = ''
    products = ''

    hot_product = get_hot_product()
    categories = ProductCategory.objects.all()
    basket = get_basket(request.user)
    same_products = get_same_products(hot_product)


    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'pk':0, 'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category_id__pk=pk).order_by('price')

        paginator =Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)





    context = {
        'title': title,
        'categories': categories,
        'category': category,
        'products': products_paginator,
        'basket': basket,
        'same_products': same_products,
        'hot_product': hot_product,
    }
    return render(request, 'products_list.html', context=context)


@login_required
def product(request, pk):
    title = 'страница продута'
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'categories': ProductCategory.objects.all(),
        'product': product,
        'basket': get_basket(request.user),
        'same_products': get_same_products(product),
    }
    return render(request, 'product.html', context)