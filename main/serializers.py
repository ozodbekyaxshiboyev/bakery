from rest_framework import serializers
from .models import (
Bread,
BreadItem,
Bakery,
Category,
)


class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BakerySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Bakery
        fields = '__all__'


class BreadSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class BreadItemSerilizer(serializers.ModelSerializer):
    class Meta:
        model = BreadItem
        fields = '__all__'
