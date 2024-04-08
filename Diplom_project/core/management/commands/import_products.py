import yaml
from django.core.management.base import BaseCommand
from core.models import Category, Product, Shop

class Command(BaseCommand):
    help = 'Imports shops, products, and categories from a YAML file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='The YAML file to import products from')

    def handle(self, *args, **kwargs):
        with open(kwargs['filename'], 'r') as file:
            data = yaml.safe_load(file)

        # Создаем или получаем магазин
        shop_name = data.get('shop')
        if shop_name:
            shop, created = Shop.objects.get_or_create(name=shop_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully processed shop {shop_name}'))

        # Обрабатываем категории
        for cat_data in data['categories']:
            Category.objects.get_or_create(id=cat_data['id'], defaults={'name': cat_data['name']})

        # Обрабатываем товары
        for prod_data in data['goods']:
            category = Category.objects.get(id=prod_data['category'])
            # Используем update_or_create для предотвращения дубликатов
            product, created = Product.objects.update_or_create(
                id=prod_data['id'],
                defaults={
                    'shop': shop,
                    'category': category,
                    'model': prod_data['model'],
                    'name': prod_data['name'],
                    'price': prod_data['price'],
                    'price_rrc': prod_data['price_rrc'],
                    'quantity': prod_data['quantity'],
                    'parameters': prod_data['parameters'],
                }
            )
            action = 'created' if created else 'updated'
            self.stdout.write(self.style.SUCCESS(f'Product {prod_data["name"]} {action}'))

        self.stdout.write(self.style.SUCCESS('Successfully imported products'))
