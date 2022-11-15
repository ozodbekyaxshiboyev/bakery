from django.urls import path,include
from rest_framework.routers import DefaultRouter

from main.views import CategoryViewset,BakeryViewset,BreadViewset,BreadItemViewset

router = DefaultRouter()
router.register('category', CategoryViewset, 'category')
router.register('bakery', BakeryViewset, 'bakery')
router.register('bread', BreadViewset, 'bread')
router.register('breaditem', BreadItemViewset, 'breaditem')

urlpatterns = [
    path('', include(router.urls)),
]
