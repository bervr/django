from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from authapp.models import ShopUser
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser

from adminapp.forms import ShopUserRegisterForm,ShopUserEditForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'Создать нового пользователя'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'adminapp/new_user.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'редактирование пользователя'
    user = ShopUser.objects.get(pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        edit_form = ShopUserEditForm(instance=user)

    content = {'title': title, 'edit_form': edit_form, 'pk': pk}

    return render(request, 'adminapp/edit.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = ShopUser.objects.get(pk=pk)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admin_staff:users'))



@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    pass

@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    pass

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    pass