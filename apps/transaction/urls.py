from django.urls import path
from .views import TransactionSeason, TransactionChart

# from .views import MemberList

app_name = "transaction"

urlpatterns = [
    # path('', MemberList.as_view(), name='list'),
    path('season/', TransactionSeason.as_view(), name='season'),
    path('chart/', TransactionChart.as_view(), name='chart'),
]
