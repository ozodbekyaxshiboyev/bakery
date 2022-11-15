from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .serializers import CategorySerilizer,BakerySerilizer,BreadSerilizer,BreadItemSerilizer
from .models import (
Bread,
BreadItem,
Bakery,
Category,
)
from .permissions import DirectorPermission,IsnotclientPermission


class CategoryViewset(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerilizer
    permission_classes = [permissions.IsAuthenticated, IsnotclientPermission]


class BakeryViewset(ModelViewSet):
    queryset = Bakery.objects.all()
    serializer_class = BakerySerilizer
    permission_classes = [permissions.IsAuthenticated,DirectorPermission]


class BreadViewset(ModelViewSet):
    queryset = Bread.objects.all()
    serializer_class = BreadSerilizer
    permission_classes = [permissions.IsAuthenticated,IsnotclientPermission]


class BreadItemViewset(ModelViewSet):
    queryset = BreadItem.objects.all()
    serializer_class = BreadItemSerilizer
    permission_classes = [permissions.IsAuthenticated,IsnotclientPermission]

