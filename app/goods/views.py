from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, category_slug):

    page = request.GET.get('page', 1)
    # Фильтры
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)

    # Реализация сортировки по категории
    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        # Вызов Page not found, если в БД ничего нет
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    # Добавление к goods отфильтрованных товаров
    if on_sale:
        goods = goods.filter(discount__gt=0)
    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    # Создание пагинатора (по 3 товара на страницу)
    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page))  # Переменная для пользователя

    context = {
        'title': 'Home - Каталог',
        'goods': current_page,
        'slug_url': category_slug,
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    contex = {
        'product': product,
    }

    return render(request, 'goods/product.html', contex)
