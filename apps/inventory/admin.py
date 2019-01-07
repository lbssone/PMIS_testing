from django.contrib import admin

from .models import Product
from .models import Component
from .models import Material
from .models import Component_detail
from .models import Material_detail

# Register your models here.
admin.site.register(Product)
admin.site.register(Component)
admin.site.register(Material)
admin.site.register(Component_detail)
admin.site.register(Material_detail)