from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, category_slug):

    # Сортировка категории
    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        # Вызов Page not found, если в БД ничего нет
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    context = {
        'title': 'Home - Каталог',
        'goods': goods,
    }
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    contex = {
        'product': product,
    }

    return render(request, 'goods/product.html', contex)
