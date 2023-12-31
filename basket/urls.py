from django.urls import path
from basket.views import *

urlpatterns = [
    path('', basket_info, name='list_basket_prod'),
    path('add/<int:product_id>/', basket_add, name='add_basket_prod'),
    path('remove/<int:product_id>/', basket_remove, name='remove_basket_prod'),
    path('clear/', basket_clear, name='clear_basket_prod'),
    path('order/', order_detail, name='order'),
]