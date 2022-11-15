from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import OrderListCreateApiView

router = DefaultRouter()
# router.register('ordetitem',OrderItemViewset,'orderitem')

urlpatterns = [
    path('',OrderListCreateApiView.as_view(),name='client_orders'),
    # path('cabinet/orders/<order_pk>/',OrderDetailApiView.as_view(),name='client_order_detail'),
    # path('cabinet/orders/<order_pk>/cancel/',cancel_order,name='client_order_cancel'),
    # path('cabinet/',include(router.urls)),
    #
    # path('orders/', OrderListCreateApiView.as_view(), name='client_orders'),

]
