from pathlib import Path

from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "Fix duplicated product image paths"


    def handle(self, *args, **options):
        products = Product.objects.exclude(image="")

        fixed = 0
        skipped = 0

        for product in products:
            old_name = product.image.name

            if not old_name:
                skipped += 1
                continue

            filename = Path(old_name).name

            new_name = f"products/{filename}"

            if old_name != new_name:
                product.image.name = new_name
                product.save(update_fields=["image"])

                fixed += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Fixed: {product.name} -> {new_name}"
                    )
                )
            else:
                skipped += 1

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished | Fixed: {fixed} | Skipped: {skipped}"
            )
        )