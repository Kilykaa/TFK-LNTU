from django.shortcuts import render


def home(request):
    context = {
        'title': 'Головна - Аптека Blin',
        'page_name': 'Головна сторінка',
        'featured_products': [
            {'name': 'Метадон', 'price': 1225.50, 'image': 'paracetamol.jpg'},
            {'name': 'Героїн', 'price': 1445.00, 'image': 'vitamin_c.jpg'},
            {'name': 'Alfa Pvp', 'price': 1818.75, 'image': 'aspirin.jpg'},
        ]
    }
    return render(request, 'pharmacy/home.html', context)


def catalog(request):
    context = {
        'title': 'Каталог товарів - Аптека Blin',
        'page_name': 'Каталог товарів',
        'categories': [
            'Знеболюючі засоби',
            'Вітаміни та БАДи',
            'Серцево-судинні препарати',
            'Засоби від застуди',
            'Органи',
        ],
        'products': [
            {
                'id': 1, 'name': 'Метадон 500мг', 'price': 1225.50,
                'category': 'Знеболюючі засоби', 'in_stock': True,
                'description': 'Ефективний знеболюючий та жарознижуючий засіб'
            },
            {
                'id': 2, 'name': 'Alfa Pvp 400мг', 'price': 1442.00,
                'category': 'Знеболюючі засоби', 'in_stock': True,
                'description': 'Протизапальний та знеболюючий препарат'
            },
            {
                'id': 3, 'name': 'Героїн 1000мг', 'price': 1665.50,
                'category': 'Вітаміни та БАДи', 'in_stock': False,
                'description': 'Для підтримки імунної системи'
            },
        ]
    }
    return render(request, 'pharmacy/catalog.html', context)


def product_detail(request, product_id):
    products_data = {
        1: {
            'id': 1, 'name': 'Метадон 500мг', 'price': 1225.50,
            'category': 'Знеболюючі засоби', 'in_stock': True,
            'description': 'Ефективний знеболюючий та жарознижуючий засіб. Рекомендується при головному болю, зубному болю, м\'язовому болю.',
            'manufacturer': 'Фармак', 'country': 'Україна',
            'dosage': '500мг', 'package': '20 таблеток'
        }
    }

    product = products_data.get(product_id, products_data[1])
    context = {
        'title': f'{product["name"]} - Аптека Blin',
        'page_name': product['name'],
        'product': product
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
    context = {
        'title': 'Про нас - Аптека Blin',
        'page_name': 'Про нашу аптеку',
        'company_info': {
            'established': 2010,
            'experience': 14,
            'locations': 5,
            'pharmacists': 12,
            'products_count': 5000,
            'description': 'Аптека Blin - надійний партнер у сфері охорони здоров\'я з 2010 року.'
        }
    }
    return render(request, 'pharmacy/about.html', context)