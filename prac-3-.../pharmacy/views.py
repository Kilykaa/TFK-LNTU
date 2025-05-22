from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def home(request):
    featured_products = Product.objects.filter(
        stock_status='in_stock'
    ).order_by('-rating', '-created_at')[:3]

    context = {
        'title': 'Головна - Аптека Blin',
        'page_name': 'Головна сторінка',
        'featured_products': featured_products,
    }
    return render(request, 'pharmacy/home.html', context)


def catalog(request):
    categories = Category.objects.filter(is_active=True)

    products = Product.objects.select_related('category').all()

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__name=category_filter)

    context = {
        'title': 'Каталог товарів - Аптека Blin',
        'page_name': 'Каталог товарів',
        'categories': categories,
        'products': products,
    }
    return render(request, 'pharmacy/catalog.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = {
        'title': f'{product.name} - Аптека Blin',
        'page_name': product.name,
        'product': product,
    }
    return render(request, 'pharmacy/product_detail.html', context)


def cart(request):
    context = {
        'title': 'Кошик - Аптека Blin',
        'page_name': 'Ваш кошик',
        'cart_items': [],  # Буде заповнено в лабі 8
        'total_price': 0
    }
    return render(request, 'pharmacy/cart.html', context)


def about(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.filter(is_active=True).count()
    in_stock_products = Product.objects.filter(stock_status='in_stock').count()

    context = {
        'title': 'Про нас - Аптека Blin',
        'page_name': 'Про нашу аптеку',
        'company_info': {
            'established': 1984,
            'experience': 41,
            'locations': 5,
            'pharmacists': 12,
            'products_count': total_products,
            'categories_count': total_categories,
            'in_stock_count': in_stock_products,
            'description': 'Аптека Blin - надійний партнер у сфері охорони здоров\'я з 1984 року.'
        }
    }
    return render(request, 'pharmacy/about.html', context)