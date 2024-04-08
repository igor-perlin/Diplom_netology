from rest_framework import serializers
from .models import Product, Order, OrderItem, Contact, Shop, Category
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'user_type')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'id', 'user', 'phone', 'email', 'first_name', 'last_name', 'middle_name',
            'city', 'street', 'house', 'building', 'structure', 'apartment'
        ]
        extra_kwargs = {'user': {'read_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_price', 'items']

    def get_total_price(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    shop_name = serializers.ReadOnlyField(source='product.shop.name')
    price = serializers.ReadOnlyField(source='product.price')
    sum = serializers.SerializerMethodField()

    def get_sum(self, obj):
        return obj.quantity * obj.product.price

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'shop_name', 'price', 'quantity', 'sum']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     parameters = serializers.JSONField()
#
#     class Meta:
#         model = Product
#         fields = ['id', 'category', 'model', 'name', 'price', 'price_rrc', 'quantity', 'parameters']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'price_rrc', 'quantity', 'parameters', 'category', 'shop']

    def create(self, validated_data):
        product, created = Product.objects.update_or_create(
            id=validated_data.get('id', None),
            defaults=validated_data,
        )
        return product

class PriceUpdateSerializer(serializers.Serializer):
    shop = serializers.CharField(max_length=255)
    categories = serializers.ListField(
        child=serializers.DictField()
    )
    goods = serializers.ListField(
        child=serializers.DictField()
    )

    def update_products(self, shop, products_data):
        Shop.objects.get_or_create(name=shop)  # Создаем магазин, если он не существует
        for product_data in products_data:
            category_data = product_data.pop('category', None)
            category, _ = Category.objects.get_or_create(id=category_data['id'], defaults={'name': category_data['name']})
            product_data['category'] = category
            product_data['shop'] = Shop.objects.get(name=shop)
            ProductSerializer().create(product_data)
