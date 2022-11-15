from django.contrib import admin

from main.models import BreadItem, Bread, Bakery, Category

admin.site.register((Category,Bakery,Bread,BreadItem,))
