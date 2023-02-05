from django.contrib import admin

# Register your models here.

from products.models import ProductCategory, Product
from users.models import User

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(User)