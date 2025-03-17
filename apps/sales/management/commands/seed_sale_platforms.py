from django.core.management.base import BaseCommand
from apps.sales.models import SalePlatform
import pathlib,json

class Command(BaseCommand):
    help = 'Seed database with sale platforms from json'

    def handle(self, *args, **kwargs):
        json_path = pathlib.Path(__file__).parent.resolve() / 'jsons' / 'sale_platforms.json'
        print(json_path)
        with open(json_path, "r", encoding="utf-8") as file:
            sale_platforms = json.load(file)
            for sale_platform in sale_platforms:
                SalePlatform.objects.get_or_create(
                    name=sale_platform['name'],
                    url=sale_platform['url']
                )

        self.stdout.write(self.style.SUCCESS('Sale Platforms created successfully!'))