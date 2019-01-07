from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView
import apps.inventory.urls as inventory_routes
import apps.member.urls as member_routes
import apps.transaction.urls as transaction_routes
import apps.activity.urls as activity_routes


urlpatterns = [
    path('', TemplateView.as_view(template_name='modules/index/index.html'), name='homepage'),
    path('inventory/', include(inventory_routes)),
    path('member/', include(member_routes)),
    path('transaction/', include(transaction_routes)),
    path('activity/', include(activity_routes)),
    path('admin/', admin.site.urls),
]
