from django.contrib import admin
from .models import *
from .models import Catagory
from .models import Product

# Register your models here.
# -------------------
# class CategoryAdmin(admin.ModelAdmin):
#     list_display =('name','image', 'discription')
# admin.site.register(Catagory,CategoryAdmin)
# -------------------

admin.site.register(Catagory)
admin.site.register(Product)
