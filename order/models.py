from django.db import models
from main.models import BaseModel, Bread, BreadItem
from main.services import validate_amount
from .enums import Status
from accounts.models import Client


class Order(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.PROTECT,related_name='order')
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=Status.choices(), default=Status.new.value)

    @property
    def get_total_cost(self):
        return sum(item.get_total_price for item in self.order_items.all())

    def __str__(self):
        return f"{self.created_date} {self.client.full_name} {self.status}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE,related_name='orderitem')
    count = models.PositiveIntegerField()
    price = models.FloatField(validators=[validate_amount])

    @property
    def get_total_price(self):
        return self.count * self.price

    def __str__(self):
        return f"{self.order} {self.bread.name} {self.count}"

