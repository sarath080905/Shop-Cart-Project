from django.db import models
import datetime
import os

def getfileName(instance, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = f"{now_time}_{filename}"
    return os.path.join('Uploads/', new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getfileName, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)  # Optional URL
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-Show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def image_or_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        elif self.image_url:
            return self.image_url
        return "/static/images/no-image.png"  # fallback placeholder


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False, blank=False)
    vendor = models.CharField(max_length=150, null=False, blank=False)
    image = models.ImageField(upload_to=getfileName, null=True, blank=True)  # File upload
    image_url = models.URLField(max_length=500, null=True, blank=True)       # Optional URL
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank=False)
    description = models.TextField(max_length=500, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0-Show,1-Hidden")
    trending = models.BooleanField(default=False, help_text="0-Show,1-Hidden") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def image_or_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        elif self.image_url:
            return self.image_url
        return "/static/images/no-image.png"  # fallback placeholder


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name}"


class Favorite(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s Favorite - {self.product.name}"
