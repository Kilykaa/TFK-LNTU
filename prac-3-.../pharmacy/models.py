from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    description = models.TextField(blank=True, verbose_name="Опис категорії")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    PRODUCT_TYPES = [
        ('medicine', 'Ліки'),
        ('organ', 'Органи'),
        ('supplement', 'БАДи'),
        ('medical_device', 'Медичні прилади'),
    ]

    COUNTRY_CHOICES = [
        ('UA', 'Україна'),
        ('US', 'США'),
        ('DE', 'Німеччина'),
        ('FR', 'Франція'),
        ('PL', 'Польща'),
        ('IN', 'Індія'),
    ]

    STOCK_STATUS = [
        ('in_stock', 'В наявності'),
        ('out_of_stock', 'Немає в наявності'),
        ('limited', 'Обмежена кількість'),
        ('pre_order', 'Під замовлення'),
    ]

    name = models.CharField(max_length=200, verbose_name="Назва товару")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    description = models.TextField(verbose_name="Опис товару")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Ціна (грн)"
    )
    manufacturer = models.CharField(
        max_length=100,
        default="Невідомий виробник",
        verbose_name="Виробник"
    )
    country = models.CharField(
        max_length=2,
        choices=COUNTRY_CHOICES,
        default='UA',
        verbose_name="Країна виробництва"
    )
    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default='medicine',
        verbose_name="Тип товару"
    )
    stock_status = models.CharField(
        max_length=20,
        choices=STOCK_STATUS,
        default='in_stock',
        verbose_name="Статус наявності"
    )
    dosage = models.CharField(
        max_length=50,
        blank=True,
        default="Не вказано",
        verbose_name="Дозування"
    )
    package = models.CharField(
        max_length=100,
        blank=True,
        default="1 упаковка",
        verbose_name="Упаковка"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        verbose_name="Рейтинг (1-5)"
    )
    is_prescription_required = models.BooleanField(
        default=False,
        verbose_name="Потрібен рецепт"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.price} грн"

    @property
    def in_stock(self):
        return self.stock_status == 'in_stock'

    def get_absolute_url(self):
        return reverse('pharmacy:product_detail', args=[self.pk])

    def get_stock_display_color(self):
        colors = {
            'in_stock': 'green',
            'out_of_stock': 'red',
            'limited': 'orange',
            'pre_order': 'blue',
        }
        return colors.get(self.stock_status, 'gray')


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('processing', 'Обробляється'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Скасовано'),
    ]

    customer_name = models.CharField(max_length=100, verbose_name="Ім'я клієнта")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон")
    customer_email = models.EmailField(blank=True, verbose_name="Email")
    delivery_address = models.TextField(verbose_name="Адреса доставки")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус замовлення"
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Загальна сума"
    )
    notes = models.TextField(blank=True, verbose_name="Примітки")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['-created_at']

    def __str__(self):
        return f"Замовлення #{self.pk} - {self.customer_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна за одиницю")

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price