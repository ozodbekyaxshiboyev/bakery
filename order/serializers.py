from rest_framework import serializers
from .enums import Status
from .models import (
Order,
OrderItem
)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order','bread','count','price',)

    def create(self, validated_data):
        OrderItem.objects.create(**validated_data)
        return validated_data


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, required=True, write_only=True)
    class Meta:
        model=Order
        fields = ('orderitems','client','address',)


    def create(self, validated_data):
        order = Order(**validated_data)
        order.save()
        print(validated_data)

        orderItemsList = validated_data.get('orderitems')
        orderItemSerializer = OrderItemSerializer(data=orderItemsList,many=True)

        if orderItemSerializer.is_valid():
            orderItemSerializer.save()

        return validated_data

#
# class OrderSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = '__all__'
#
#
# class OrderClientSerilizer(serializers.ModelSerializer):  # todo patch va putda qanday uzgartiriladi
#     class Meta:
#         model = Order
#         fields = ('id','client','address',)
#
#     def update(self, instance, validated_data):
#         if instance.status != Status.new.value:
#             raise serializers.ValidationError({"Xatolik":"Ko`rib chiqilgan buyurtmani uzgartirib bo`lmaydi!"})
#         instance.address = validated_data.get('address',instance.address)
#         instance.save()
#         return instance
#
#
# class OrderBakerSerilizer(serializers.ModelSerializer):  # todo patch va putda qanday uzgartiriladi
#     class Meta:
#         model = Order
#         fields = ('id','status',)
#
#     def update(self, instance, validated_data):
#         if validated_data.get('status') == Status.new.value:
#             raise serializers.ValidationError({"Xatolik":"Buyurtman dastlabki holatga qaytarib bo`lmaydi!"})
#         instance.status = validated_data.get('status')
#         instance.save()
#         return instance
#
#
# class OrderItemSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

