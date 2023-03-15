from django.shortcuts import render, HttpResponseRedirect
from products.models import ProductCategory, Product, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, TemplateView, CreateView
from users.models import User
from common.views import TitleMixin


# Create your views here.

class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     context['title'] = 'Store'
    #     return context


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    basket = Basket.objects.filter(user=request.user, product=product)

    if not basket.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = basket.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def index(request):
#     context = {'title': 'Store'}
#     return render(request, 'products/index.html', context)


# def products(request, category_id=None):
#     if category_id:
#         products_paginator = Product.objects.filter(category_id=category_id)
#     else:
#         products_paginator = Product.objects.all()
#     prod_all = Product.objects.all()
#     per_page = 3
#     paginator = Paginator(prod_all, per_page)
#     page_num = request.GET.get('page', 1)
#     products_paginator = paginator.get_page(page_num)
#     context = {'title': 'Store - Каталог',
#                'categories': ProductCategory.objects.all(),
#                'products': products_paginator,
#                }
#     return render(request, 'products/products.html', context)
