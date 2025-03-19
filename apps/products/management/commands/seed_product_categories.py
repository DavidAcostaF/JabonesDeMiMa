from django.core.management.base import BaseCommand
from apps.products.models import ProductCategory
import pathlib
import json

class Command(BaseCommand):
    help = 'Seed database with product categories for health products'

    def handle(self, *args, **kwargs):
        json_path = pathlib.Path(__file__).parent.resolve() / 'jsons' / 'product_categories.json'
        print(json_path)
        with open(json_path, "r", encoding="utf-8") as file:
            categories = json.load(file)
            for category in categories:
                ProductCategory.objects.get_or_create(name=category['name'])

        self.stdout.write(self.style.SUCCESS('Product categories created successfully!'))
