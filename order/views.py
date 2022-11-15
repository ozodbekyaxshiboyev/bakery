from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,\
    RetrieveUpdateDestroyAPIView,CreateAPIView,RetrieveUpdateAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status

from .enums import Status
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order,OrderItem
from main.permissions import DirectorPermission,IsnotclientPermission,IsClient,IsOwner
from rest_framework.decorators import api_view,permission_classes


class OrderListCreateApiView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer











    # permission_classes = [IsClient]

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     queryset = queryset.filter(client=request.user)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)


# class OrderDetailApiView(RetrieveUpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderClientSerilizer
#     permission_classes = [IsClient,IsOwner]
#     lookup_field = 'order_pk'
#
#
# @api_view(http_method_names=['post'])
# @permission_classes([IsOwner,IsClient])
# def cancel_order(request,order_pk):
#     order = Order.objects.get(pk=order_pk)
#     if order:
#         order.status = Status.cancelled.value
#         return Response(status=status.HTTP_200_OK)
#     return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class OrderItemViewset(ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerilizer
#     permission_classes = [IsClient]
#
#
# class OrderListApiView(ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerilizer
#     permission_classes = [IsnotclientPermission]
#
#
# class OrderChangeApiView(RetrieveUpdateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderBakerSerilizer
#     permission_classes = [IsnotclientPermission]
#     lookup_field = 'order_pk'


