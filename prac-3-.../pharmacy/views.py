from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category, Order, OrderItem
from decimal import Decimal
import json


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
    cart_items = request.session.get('cart', {})
    products = []
    total_price = 0

    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total_price += item_total
            products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
        except Product.DoesNotExist:
            continue

    context = {
        'title': 'Кошик - Аптека Blin',
        'page_name': 'Ваш кошик',
        'cart_items': products,
        'total_price': total_price,
        'has_items': bool(products)
    }
    return render(request, 'pharmacy/cart.html', context)


@csrf_exempt
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        product = get_object_or_404(Product, id=product_id)

        if product.stock_status != 'in_stock':
            return JsonResponse({'success': False, 'message': 'Товар недоступний'})

        cart = request.session.get('cart', {})
        product_id_str = str(product_id)

        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity

        request.session['cart'] = cart
        request.session.modified = True

        cart_count = sum(cart.values())

        return JsonResponse({
            'success': True,
            'message': 'Товар додано до кошика',
            'cart_count': cart_count
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Помилка при додаванні до кошика'})


@csrf_exempt
@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))

        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            request.session.modified = True

        cart_count = sum(cart.values())

        return JsonResponse({
            'success': True,
            'message': 'Товар видалено з кошика',
            'cart_count': cart_count
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Помилка при видаленні з кошика'})


@csrf_exempt
@require_POST
def update_cart(request):
    try:
        data = json.loads(request.body)
        product_id = str(data.get('product_id'))
        quantity = data.get('quantity', 1)

        if quantity <= 0:
            return remove_from_cart(request)

        cart = request.session.get('cart', {})
        cart[product_id] = quantity
        request.session['cart'] = cart
        request.session.modified = True

        cart_count = sum(cart.values())

        return JsonResponse({
            'success': True,
            'message': 'Кількість оновлено',
            'cart_count': cart_count
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Помилка при оновленні кошика'})


def checkout(request):
    cart_items = request.session.get('cart', {})

    if not cart_items:
        messages.error(request, 'Кошик порожній')
        return redirect('pharmacy:cart')

    products = []
    total_price = 0

    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=int(product_id))
            item_total = product.price * quantity
            total_price += item_total
            products.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
        except Product.DoesNotExist:
            continue

    context = {
        'title': 'Оформлення замовлення - Аптека Blin',
        'page_name': 'Оформлення замовлення',
        'cart_items': products,
        'total_price': total_price
    }
    return render(request, 'pharmacy/checkout.html', context)


@require_POST
def place_order(request):
    cart_items = request.session.get('cart', {})

    if not cart_items:
        messages.error(request, 'Кошик порожній')
        return redirect('pharmacy:cart')

    customer_name = request.POST.get('customer_name')
    customer_phone = request.POST.get('customer_phone')
    customer_email = request.POST.get('customer_email', '')
    delivery_address = request.POST.get('delivery_address')
    notes = request.POST.get('notes', '')

    if not all([customer_name, customer_phone, delivery_address]):
        messages.error(request, 'Заповніть всі обов\'язкові поля')
        return redirect('pharmacy:checkout')

    total_amount = Decimal('0.00')
    order_items = []

    for product_id, quantity in cart_items.items():
        try:
            product = Product.objects.get(id=int(product_id))
            if product.stock_status != 'in_stock':
                messages.error(request, f'Товар {product.name} недоступний')
                return redirect('pharmacy:cart')

            item_total = product.price * quantity
            total_amount += item_total
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        except Product.DoesNotExist:
            continue

    if not order_items:
        messages.error(request, 'Немає доступних товарів для замовлення')
        return redirect('pharmacy:cart')

    order = Order.objects.create(
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_email=customer_email,
        delivery_address=delivery_address,
        notes=notes,
        total_amount=total_amount,
        status='pending'
    )

    for item in order_items:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['price']
        )

    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, f'Замовлення #{order.pk} успішно оформлено!')
    return redirect('pharmacy:order_success', order_id=order.pk)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    context = {
        'title': 'Замовлення оформлено - Аптека Blin',
        'page_name': 'Замовлення успішно оформлено',
        'order': order
    }
    return render(request, 'pharmacy/order_success.html', context)


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