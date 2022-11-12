from django.db import models
from accounts.models import User,Director,Vendor,Baker,Client
from django.db.models import Model
from django.core.exceptions import ValidationError
from phonenumber_field import modelfields
from .enums import Status
from .services import validate_amount



class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False,blank=True, null=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='child')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='category')


    def __str__(self):
        return self.name

class Bakery(BaseModel):
    owner = models.ForeignKey(Director, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = modelfields.PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    open_at = models.TimeField()
    close_at = models.TimeField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='bakery')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'address'], name="name-address")
        ]

    def __str__(self):
        return self.name


class Bread(BaseModel):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='bread')
    price = models.DecimalField(validators=[validate_amount])
    description = models.CharField(max_length=300, default="nothing is to describe")
    image = models.ImageField(upload_to='bread/images')
    kg = models.FloatField(validators=[validate_amount],blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='bread')


    def __str__(self):
        return self.name


class BreadItem(BaseModel):
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE, related_name='breaditem')
    count = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='breaditem')


    def __str__(self):
        return f"{self.bread.name} {self.count}"


class Order(BaseModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='order')
    status = models.CharField(max_length=20, choices=Status.choices())

    def get_total_cost(self):
        return sum(item.get_total_price() for item in self.order_items.all())

    def __str__(self):
        return f"{self.created_date} {self.client.full_name} {self.status}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE,related_name='orderitem')
    count = models.PositiveIntegerField()
    price = models.DecimalField(validators=[validate_amount])

    def get_total_price(self):
        return self.count * self.price

    def __str__(self):
        return f"{self.order} {self.bread.name} {self.count}"

