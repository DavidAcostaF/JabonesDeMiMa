from django.core.management.base import BaseCommand
from apps.products.models import Product, ProductCategory
import pathlib
import json

class Command(BaseCommand):
    help = 'Seed database with products for health products'

    def handle(self, *args, **kwargs):
        json_path = pathlib.Path(__file__).parent.resolve() / 'jsons' / 'products.json'
        print(json_path)
        
        with open(json_path, "r", encoding="utf-8") as file:
            products = json.load(file)
            
            for product in products:
                category = ProductCategory.objects.get(name=product['category_name'])
                
                Product.objects.get_or_create(
                    name=product['name'],
                    price=product['price'],
                    stock=product['stock'],
                    category=category
                )

        self.stdout.write(self.style.SUCCESS('Products created successfully!'))
