from django.contrib import admin

from order.models import OrderItem, Order

admin.site.register((Order,OrderItem,))
