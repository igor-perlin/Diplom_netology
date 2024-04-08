from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets, filters, views
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Order, OrderItem, Contact, Shop, User, Supplier, Category
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    OrderItemSerializer,
    UserRegistrationSerializer,
    CartItemSerializer,
    ContactSerializer,
    ShopSerializer
)
from .filters import ProductFilter
from django.core.mail import send_mail
from .models import PasswordResetToken
from .serializers import PriceUpdateSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ['name', 'model']
    filterset_class = ProductFilter

class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Отправляем email с подтверждением
            send_mail(
                'Подтверждение регистрации',
                'Вы успешно зарегистрировались.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    """
    Класс для управления корзиной: добавление товаров, их удаление и просмотр содержимого корзины.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Предположим, что статус 'basket' используется для корзины
        cart = Order.objects.filter(user=request.user, status='basket').first()
        if not cart:
            return Response([])
        items = OrderItem.objects.filter(order=cart)
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)
        # order = Order.objects.filter(user=request.user, status='basket').first()
        # if order:
        #     items = order.items.all()
        #     serializer = CartItemSerializer(items, many=True)
        #     return Response(serializer.data)
        # return Response([], status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = get_object_or_404(Product, pk=product_id)
        order, _ = Order.objects.get_or_create(user=request.user, status='basket')
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            order_item.quantity += int(quantity)
            order_item.save()
        return Response({'detail': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        order = Order.objects.filter(user=request.user, status='basket').first()
        if not order:
            return Response({'detail': 'Корзина пуста'}, status=status.HTTP_404_NOT_FOUND)
        product = get_object_or_404(Product, pk=product_id)
        order_item = get_object_or_404(OrderItem, order=order, product=product)
        order_item.delete()
        return Response({'detail': 'Товар удален из корзины'}, status=status.HTTP_204_NO_CONTENT)

class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращает контакты только для текущего пользователя.
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращает список заказов только для текущего пользователя.
        return Order.objects.filter(user=self.request.user)

class ConfirmOrderView(APIView):
    """
    Класс для подтверждения заказа через POST-запрос.
    """
    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        contact_id = request.data.get('contact_id')

        try:
            order = Order.objects.get(id=order_id, user=request.user)
            contact = Contact.objects.get(id=contact_id, user=request.user)
            order.contact = contact
            order.status = 'confirmed'
            order.save()
            return Response({'detail': 'Заказ подтвержден'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or does not belong to the user.'}, status=status.HTTP_404_NOT_FOUND)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found or does not belong to the user.'}, status=status.HTTP_404_NOT_FOUND)

class ShopView(APIView):
    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(views.APIView):
    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Создаем токен сброса и отправляем на email
            token = PasswordResetToken.objects.create(user=user)
            reset_link = f'http://example.com/reset_password/{token.token}/'
            send_mail(
                'Password Reset',
                f'Please follow the link to reset your password: {reset_link}',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return Response({'detail': 'Please check your email for the password reset link.'})
        return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetView(views.APIView):
    def post(self, request, token):
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            user = reset_token.user
            user.set_password(request.data.get('password'))
            user.save()
            reset_token.delete()  # Удаляем токен после успешного сброса
            return Response({'detail': 'Password has been reset successfully.'})
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_404_NOT_FOUND)

# Обновление прайса через

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_price(request):
    user = request.user
    # Проверяем, является ли пользователь поставщиком
    if user.user_type != 'supplier':
        return Response({"detail": "Только поставщики могут обновлять прайс-листы."}, status=403)

    serializer = PriceUpdateSerializer(data=request.data)
    if serializer.is_valid():
        shop_name = serializer.validated_data.get('shop')
        shop = get_object_or_404(Shop, name=shop_name, owner=user)

        # Обновляем категории
        for category_data in serializer.validated_data.get('categories', []):
            Category.objects.update_or_create(
                id=category_data['id'],
                defaults={'name': category_data['name']}
            )

        # Обновляем товары
        for product_data in serializer.validated_data.get('goods', []):
            category = get_object_or_404(Category, id=product_data['category'])
            # Обновляем или создаем новый товар
            product, created = Product.objects.update_or_create(
                id=product_data['id'],
                defaults={
                    'shop': shop,
                    'category': category,
                    'model': product_data.get('model'),
                    'name': product_data['name'],
                    'price': product_data['price'],
                    'price_rrc': product_data.get('price_rrc', 0),
                    'quantity': product_data['quantity'],
                    'parameters': product_data.get('parameters', {})
                }
            )

        return Response({"detail": "Прайс-лист успешно обновлен."})
    else:
        return Response(serializer.errors, status=400)


# Включение/выключение приёма заказов

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_order_acceptance(request):
    user = request.user
    # Проверяем, является ли пользователь поставщиком
    if not hasattr(user, 'supplier'):
        return Response({"detail": "Только поставщики могут изменять статус приёма заказов."}, status=403)

    supplier = get_object_or_404(Supplier, user=user)
    supplier.is_accepting_orders = not supplier.is_accepting_orders
    supplier.save()

    return Response({"is_accepting_orders": supplier.is_accepting_orders})

# Получение списка заказов

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    user = request.user
    if user.user_type != 'supplier':
        return Response({"detail": "Только поставщики могут видеть заказы."}, status=403)

    shops = Shop.objects.filter(owner=user)
    # Предположим, что у вас есть модель Order, связанная с Shop
    orders = Order.objects.filter(shop__in=shops).distinct()


