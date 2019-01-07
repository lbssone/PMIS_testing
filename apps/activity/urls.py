from django.urls import path

from .views import ActivityDetail

app_name = "activity"

urlpatterns = [
    path('', ActivityDetail.as_view(), name='detail'),
    # path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    # path('schedule', ScheduleForm.as_view(), name='schedule_form'),
]
