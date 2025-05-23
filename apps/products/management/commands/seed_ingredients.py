from django.core.management.base import BaseCommand
from apps.products.models import Ingredient
import pathlib
import json

class Command(BaseCommand):
    help = 'Seed database with ingredients'

    def handle(self, *args, **kwargs):
        json_path = pathlib.Path(__file__).parent.resolve() / 'jsons' / 'ingredients.json'
        print(f'Loading ingredients from: {json_path}')
        
        with open(json_path, "r", encoding="utf-8") as file:
            ingredients = json.load(file)
            
            for ing in ingredients:
                Ingredient.objects.get_or_create(
                    name=ing['name'],
                    defaults={
                        'measure_unit': ing['measure_unit'],
                        'stock': ing['stock']
                    }
                )

        self.stdout.write(self.style.SUCCESS('Ingredients created successfully!'))
