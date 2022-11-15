from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import OrderListCreateApiView,OrderDetailApiView,cancel_order

router = DefaultRouter()


urlpatterns = [
    path('cabinet/orders/',OrderListCreateApiView.as_view(),name='client_orders'),
    path('cabinet/orders/<order_pk>/',OrderDetailApiView.as_view(),name='client_order_detail'),
    path('cabinet/orders/<order_pk>/cancel/',cancel_order,name='client_order_cancel'),
]
