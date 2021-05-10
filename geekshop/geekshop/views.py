from django.shortcuts import render
from mainapp.models import Product, ProductCategory
# Create your views here.

products = Product.objects.all()[:4]
products_category = ProductCategory.objects.all()[:4]
do_active = {'links': [
            {'href': '/', 'name': 'домой'},
            {'href': '/products/', 'name': 'продукты'},
            {'href': '/contacts/', 'name':'контакты'},],
            'products': products,
            'products_category':products_category,
            }

def main(request):
    return render(request, 'index.html', context=do_active)


def contacts(request):
    return render(request, 'contacts.html', context=do_active)
