from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from adminapp.forms import ShopUserRegisterForm, ShopUserEditForm, ProductCategoryEditForm, ProductCategoryCreateForm, ProductEditForm


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    # exclude = ['password']
    template_name = 'adminapp/edit.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_staff:users')
    fields = ('username','first_name', 'last_name') #'__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/new_user.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'создание категории'})
        return context

class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_staff:users')

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(ShopUser, pk=pk)
        if request.method == 'POST':
            user.is_active = False
            user.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Удаление пользователя'})
        return context



class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('admin_staff:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'создание категории'})
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    context_object_name = 'category'
    success_url = reverse_lazy('admin_staff:categories')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'изменение категории'})
        return context


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(ProductCategory, pk=pk)
        if request.method == 'POST':
            category.is_active = False
            category.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Удаление категории'})
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        category = get_object_or_404(ProductCategory, pk= pk)
        context.update({'title': 'Продукты категории',
                        'category': category,
                        'pk': pk
                        })
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product.html'
    form_class = ProductEditForm

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        initial = initial.copy()
        pk = self.kwargs.get('pk')
        initial['category'] = ProductCategory.objects.get(pk= pk)
        return initial

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        return reverse('admin_staff:products', args=[pk])

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        category = ProductCategory.objects.get(pk= pk)
        context.update({'title': 'новый продукт',
                        'category': category,
                        'pk': pk,
                        })
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = ' о продукте'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title,
               'object': product,
               }

    return render(request, 'adminapp/product_about.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[product.pk]))
    else:
        product_form = ProductEditForm(instance=product)
    context = {'title': title,
               'product_form': product_form,
               'product': product
               }

    return render(request, 'adminapp/product.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    category_pk = product.category.pk
    product.is_active = False
    product.save()
    return HttpResponseRedirect(reverse('admin_staff:products', args=[category_pk]))
