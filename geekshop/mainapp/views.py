from django.shortcuts import render


# Create your views here.
do_active = {'links': [
            {'href': '/', 'name': 'домой'},
            {'href': '/products/', 'name': 'продукты'},
            {'href': '/contacts/', 'name':'контакты'},
        ]}

def products(request):
    return render(request, 'products.html', context = do_active)

