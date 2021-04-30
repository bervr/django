from django.shortcuts import render
# Create your views here.
do_active = {'links': [
            {'href': '/', 'name': 'домой'},
            {'href': '/products/', 'name': 'продукты'},
            {'href': '/contacts/', 'name':'контакты'},
        ]}

def main(request):
    return render(request, 'index.html', context=do_active)


def contacts(request):
    return render(request, 'contacts.html', context=do_active)
