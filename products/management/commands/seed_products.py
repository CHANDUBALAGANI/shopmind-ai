import random

from django.core.management.base import BaseCommand

from products.models import Product, Category


class Command(BaseCommand):
    help = "Generate sample products"

    def handle(self, *args, **kwargs):

        if Category.objects.count() == 0:
            self.stdout.write(
                self.style.ERROR(
                    "Please create categories first."
                )
            )
            return

        product_names = [

            "Apple iPhone 16 Pro",
            "Samsung Galaxy S25",
            "OnePlus 14",
            "Google Pixel 10",
            "Xiaomi 16 Ultra",

            "Dell Inspiron 15",
            "HP Pavilion Gaming",
            "Lenovo ThinkPad X1",
            "MacBook Air M5",
            "Asus ROG Zephyrus",

            "Sony WH-1000XM6",
            "Boat Airdopes 311",
            "JBL Flip 7",
            "Apple Watch Series 11",
            "Samsung Galaxy Watch 8",

            "Logitech MX Master 3S",
            "Redragon Mechanical Keyboard",
            "Canon EOS R10",
            "GoPro Hero 15",
            "Amazon Kindle Paperwhite"

        ]

        categories = list(Category.objects.all())

        created = 0

        for i in range(100):

            Product.objects.create(

                category=random.choice(categories),

                name=random.choice(product_names) + f" #{i+1}",

                description="High-quality product generated automatically for testing.",

                price=random.randint(999, 150000),

                stock=random.randint(1, 50),

            )

            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{created} products created successfully!"
            )
        )
        