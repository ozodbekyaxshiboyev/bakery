from rest_framework import serializers
from .enums import Status
from .models import (
Order,
OrderItem
)


class OrderSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderClientSerilizer(serializers.ModelSerializer):  # todo patch va putda qanday uzgartiriladi
    class Meta:
        model = Order
        fields = ('id','client','address',)

    def update(self, instance, validated_data):
        if instance.status != Status.new.value:
            raise serializers.ValidationError({"Xatolik":"Ko`rib chiqilgan buyurtmani uzgartirib bo`lmaydi!"})
        instance.address = validated_data.get('address',instance.address)
        instance.save()
        return instance


class OrderBakerSerilizer(serializers.ModelSerializer):  # todo patch va putda qanday uzgartiriladi
    class Meta:
        model = Order
        fields = ('id','status',)

    def update(self, instance, validated_data):
        if validated_data.get('status') == Status.new.value:
            raise serializers.ValidationError({"Xatolik":"Buyurtman dastlabki holatga qaytarib bo`lmaydi!"})
        instance.status = validated_data.get('status')
        instance.save()
        return instance


class OrderItemSerilizer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

