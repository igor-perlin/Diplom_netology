from django.contrib import admin
from .models import Product, Order, OrderItem, User, Contact, Shop
from django.contrib.auth.admin import UserAdmin

from Diplom_project.my_admin_site import my_admin_site


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]

class ContactAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'email', 'city', 'street', 'house', 'building', 'structure', 'apartment')
    list_filter = ('city', 'user')
    search_fields = ('user__email', 'phone', 'city')

class CustomUserAdmin(UserAdmin):
    # Поля, используемые для отображения пользователей
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    # Поле, используемое для входа в систему
    ordering = ('email',)
    # Поля, используемые при создании/изменении пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Поля формы добавления пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    # Указываем, по какому полю искать в админке
    search_fields = ('email',)
    # Указываем, по каким полям фильтровать пользователей в админке
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

# Регистрируем модель
admin.site.register(Shop)
admin.site.register(Contact, ContactAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

# my_admin_site.register(MyModel)
my_admin_site.register(Shop)
my_admin_site.register(Contact, ContactAdmin)
my_admin_site.register(User, CustomUserAdmin)
my_admin_site.register(Product)
my_admin_site.register(Order, OrderAdmin)
my_admin_site.register(OrderItem)