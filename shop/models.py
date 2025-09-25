from django.db import models
import datetime
import os

# Create your models here.

def getfileName(request, filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('Uplpads/',new_filename)

class Category(models.Model):
    name = models.CharField(max_length=150,null=False,blank=False)
    # image = models.ImageField(upload_to=getfileName null=True,blank=True) --------  old version
    image = models.ImageField(upload_to=getfileName, null=True, blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    # trending = models.BooleanField(default=False,help_text="0-Show,1-Hidden") 
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=150,null=False,blank=False)
    vendor = models.CharField(max_length=150,null=False,blank=False)
    # Product_image = models.ImageField(upload_to=getfileName null=True,blank=True) ---- old version
    Product_image = models.ImageField(upload_to=getfileName, null=True, blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    original_price = models.FloatField(null=False,blank=False)
    selling_price = models.FloatField (null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    trending = models.BooleanField(default=False,help_text="0-Show,1-Hidden") 
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

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