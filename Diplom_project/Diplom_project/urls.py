"""
URL configuration for Diplom_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views as app_views
from core.views import UserRegistrationAPIView
from core.views import CartView
from core.views import OrderViewSet
from core.views import ConfirmOrderView
from core.views import ShopView
from core.views import PasswordResetRequestView, PasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import update_price, toggle_order_acceptance, get_orders
from .my_admin_site import my_admin_site




# Создаем экземпляр маршрутизатора
router = DefaultRouter()

# Регистрируем viewsets
router.register(r'products', app_views.ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'contacts', app_views.ContactViewSet, basename='contacts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', CartView.as_view(), name='cart_add'),
    path('cart/remove/', CartView.as_view(), name='cart_remove'),
    path('orders/confirm/', ConfirmOrderView.as_view(), name='confirm_order'),
    path('shops/', ShopView.as_view(), name='shop-list'),
    path('request_password_reset/', PasswordResetRequestView.as_view(), name='request_password_reset'),
    path('reset_password/<uuid:token>/', PasswordResetView.as_view(), name='reset_password'),
    path('api/supplier/update_price/', update_price, name='update_price'),
    path('api/toggle_order_acceptance/', toggle_order_acceptance, name='toggle_order_acceptance'),
    path('api/supplier/orders/', get_orders, name='supplier-orders'),
    path('my_admin/', my_admin_site.urls),
    path('', include(router.urls)),
]
