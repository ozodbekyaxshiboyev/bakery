from django.db import models
from accounts.models import User,Director,Vendor,Baker,Client, Staff
from django.db.models import Model
from django.core.exceptions import ValidationError
from phonenumber_field import modelfields
from .services import validate_amount
from accounts.enums import UserRoles


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False,blank=True, null=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,related_name='child',limit_choices_to={"is_deleted":False})
    creator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True,  related_name='category')

    @property
    def is_parent(self):
        return self.parent is None

    def clean(self):
        if not self.creator:
            raise ValidationError("Creatori yuq!")


    def __str__(self):
        return self.name

class Bakery(BaseModel):
    owner = models.ForeignKey(Director, on_delete=models.CASCADE,related_name='bakery_owner')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = modelfields.PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    open_at = models.TimeField()
    close_at = models.TimeField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'address'], name="name-address")
        ]

    def __str__(self):
        return self.name


class Bread(BaseModel):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='bread')
    description = models.CharField(max_length=300, default="nothing is to describe")
    image = models.ImageField(upload_to='bread/images')
    creator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='bread')

    def __str__(self):
        return self.name


class BreadItem(BaseModel):
    comment = models.CharField(max_length=200,null=True,blank=True)
    bread = models.ForeignKey(Bread, on_delete=models.CASCADE, related_name='breaditem')
    price = models.FloatField(validators=[validate_amount])
    kg = models.FloatField(validators=[validate_amount], blank=True, null=True)
    count_come = models.PositiveIntegerField()
    count_last = models.PositiveIntegerField(null=True,blank=True)
    creator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='bread_item')

    def save(self, *args, **kwargs):
        self.count_last = self.count_come
        super(BreadItem, self).save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.bread.name} {self.count_last}"
