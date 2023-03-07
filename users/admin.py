from django.contrib import admin

from users.models import User
from products.admin import BasketAdmin

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)
