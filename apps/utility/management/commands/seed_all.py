from django.core.management.base import BaseCommand
from django.core.management import call_command

import time

class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        start = time.time()
        call_command("seed_sale_platforms")
        self.stdout.write(f"seed_sale_platforms: {time.time() - start}s")

        call_command("seed_product_categories")
        self.stdout.write(f"seed_product_categories: {time.time() - start}s")
        
        call_command("seed_products")
        self.stdout.write(f"seed_products: {time.time() - start}s")
        self.stdout.write(self.style.SUCCESS("Seeded all tables successfully"))