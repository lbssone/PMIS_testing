from django.urls import path

from .views import InventoryList, ProductDetail, ScheduleForm

app_name = "inventory"

urlpatterns = [
    path('', InventoryList.as_view(), name='list'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('schedule', ScheduleForm.as_view(), name='schedule_form'),
]
