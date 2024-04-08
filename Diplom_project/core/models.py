from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from django.conf import settings
import uuid
from django.utils.formats import date_format

# Модели для поставщика и связь с магазинами (один поставщик может иметь не один магазин)

class Supplier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Используем AUTH_USER_MODEL
    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_accepting_orders = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# class Shop(models.Model):
#     name = models.CharField(max_length=255)
#     url = models.URLField()
#
#     def __str__(self):
#         return self.name
# class Shop(models.Model):
#     name = models.CharField(max_length=255)
#     owner = models.ForeignKey(User, related_name="shops", on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name

class Shop(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="shops", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

# Модель Category
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Модель Product
class Product(models.Model):
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)  # Добавляем это поле
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    parameters = JSONField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=20, default='unconfirmed')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        user = self.order.user
        full_name = user.get_full_name() or user.username
        email = user.email
        order_date = date_format(self.order.created_at, "SHORT_DATETIME_FORMAT")
        return f'Order #{self.order.id} - {full_name} ({email}), {order_date}'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    USER_TYPE_CHOICES = (
        ('supplier', 'Поставщик'),
        ('buyer', 'Покупатель'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email



# Модель Контактов

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contacts', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField()  # Добавляем поле Email
    first_name = models.CharField(max_length=30)  # Имя
    last_name = models.CharField(max_length=30)  # Фамилия
    middle_name = models.CharField(max_length=30, blank=True, null=True)  # Отчество (необязательно)
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=10)
    building = models.CharField(max_length=10, blank=True, null=True)  # Корпус (необязательно)
    structure = models.CharField(max_length=10, blank=True, null=True)  # Строение (необязательно)
    apartment = models.CharField(max_length=10, blank=True, null=True)  # Квартира (необязательно)

    def __str__(self):
        return f'{self.city}, {self.street}, {self.house}'

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)





