from io import BytesIO

from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            try:
                image = Image.open(self.image)

                # Convert images with transparency to RGB
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")

                # Resize large images
                max_size = (800, 800)
                image.thumbnail(max_size)

                # Save the processed image in memory
                output = BytesIO()

                image.save(
                    output,
                    format="JPEG",
                    optimize=True,
                    quality=75
                )

                output.seek(0)

                # Keep the existing filename but use .jpg
                original_name = self.image.name
                filename = original_name.rsplit(".", 1)[0] + ".jpg"

                self.image = ContentFile(
                    output.read(),
                    name=filename
                )

            except Exception as e:
                print(f"Image processing skipped: {e}")

        super().save(*args, **kwargs)


class Cart(models.Model):
    session_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"