from pathlib import Path
import re

from django.core.files import File
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = "Upload existing local product images to Cloudinary"

    def handle(self, *args, **options):
        base_dir = Path("media/products")

        if not base_dir.exists():
            self.stdout.write(
                self.style.ERROR("media/products folder not found.")
            )
            return

        products = Product.objects.exclude(image="")

        local_files = [
            file for file in base_dir.iterdir()
            if file.is_file()
        ]

        uploaded = 0
        missing = 0
        failed = 0

        for product in products:

            database_name = Path(product.image.name).name

            # First try exact filename
            local_path = base_dir / database_name

            # If exact filename doesn't exist,
            # match generated ChatGPT image names by timestamp.
            if not local_path.exists():

                timestamp_match = re.search(
                    r"(ChatGPT_Image_[A-Za-z0-9_]+_\d{2}_\d{2}_\d{2}_(?:AM|PM))",
                    database_name,
                    re.IGNORECASE,
                )

                if timestamp_match:
                    timestamp_part = timestamp_match.group(1)

                    matching_files = [
                        file
                        for file in local_files
                        if file.stem.lower() == timestamp_part.lower()
                    ]

                    if matching_files:
                        local_path = matching_files[0]

                # Try other filenames by removing generated suffixes
                if not local_path.exists():
                    database_stem = Path(database_name).stem

                    matching_files = [
                        file
                        for file in local_files
                        if file.stem.lower().startswith(
                            database_stem.lower()
                        )
                        or database_stem.lower().startswith(
                            file.stem.lower()
                        )
                    ]

                    if matching_files:
                        local_path = matching_files[0]

            # Still not found
            if not local_path.exists():
                missing += 1

                self.stdout.write(
                    self.style.WARNING(
                        f"Missing image: {product.name} -> "
                        f"{database_name}"
                    )
                )

                continue

            try:
                with open(local_path, "rb") as image_file:

                    product.image.save(
                        local_path.name,
                        File(image_file),
                        save=True,
                    )

                uploaded += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Uploaded: {product.name} "
                        f"<- {local_path.name}"
                    )
                )

            except Exception as e:
                failed += 1

                self.stdout.write(
                    self.style.ERROR(
                        f"Failed: {product.name} -> {e}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Finished | Uploaded: {uploaded} | "
                f"Missing: {missing} | Failed: {failed}"
            )
        )