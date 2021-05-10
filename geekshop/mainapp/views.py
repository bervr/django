from django.shortcuts import render
from mainapp.models import Product, ProductCategory
# Create your views here.


products = Product.objects.all()[:4]
products_category = ProductCategory.objects.all()
do_active = {'links': [
            {'href': '/', 'name': 'домой'},
            {'href': '/products/', 'name': 'продукты'},
            {'href': '/contacts/', 'name':'контакты'},],
            'products': products,
            'products_category' : products_category,
            }

def products(request, pk=None):
    # print(pk)
    do_active['now_category'] = pk
    return render(request, 'products.html', context = do_active)

