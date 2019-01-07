from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from datetime import datetime, timedelta

from .models import Product, Component, Material

# Create your views here.
class InventoryList(TemplateView):
    template_name = 'modules/inventory/inventory.html'

    def get_context_data(self, **kwargs):
        context = super(InventoryList, self).get_context_data(**kwargs)
        context['product_list'] = Product.objects.all()
        context['component_list'] = Component.objects.all()
        context['material_list'] = Material.objects.all()
        return context
    # model = Product, Component, Material

    # def get(self, request):
    #     product_list = Product.objects.all()
    #     component_list = Component.objects.all()
    #     material_list = Material.objects.all()
    #     return render(request, 'modules/inventory/inventory.html', {'product_list': product_list, 'component_list': component_list, 'material_list': material_list})


class ProductDetail(DetailView):
    model = Product
    template_name = 'modules/inventory/product_detail.html'
    context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetail, self).get_context_data(**kwargs)
    #     context['components_required'] = Product.getComponents(self)
    #     return context


class ScheduleForm(View):
    def get(self, request):
        return render(request, 'modules/inventory/schedule_form.html')

    def post(self, request):
        get_um = self.request.POST.get('umbrella')
        num = int(self.request.POST.get('num_of_umbrella'))
        date = self.request.POST.get('date')
        date_1 = datetime.strptime(date, "%Y-%m-%d").date()
        umbrella = ""
        if get_um == "抗UV直傘":
            umbrella = Product.objects.get(number="1")
        elif get_um == "防風直傘":
            umbrella = Product.objects.get(number="2")
        elif get_um == "輕量直傘":
            umbrella = Product.objects.get(number="3")
        component_tree_list = []
        material_list = []
        plastic = 0
        frp = 0
        fabric = 0
        plastic_date_lst = []
        frp_date_lst = []
        fabric_date = None
        for component in umbrella.components_required.all():
            component_wanted = component.number_needed*num
            component_diff = component_wanted - component.inventory
            produce_date = date_1 - timedelta(days=component.component_detail.lead_time)
            produce_date_str = str(date_1 - timedelta(days=component.component_detail.lead_time))
            # component_tree_list.append([component.name, component.number_needed, component.weight, component_wanted, component.inventory, component_quan])
            component_tree_list.append([component, component_wanted, component_diff, produce_date_str])
            if component.required_material not in material_list:
                material_list.append(component.required_material)
            if component.required_material.name == "塑膠":
                if component_diff > 0:
                    plastic += (component.weight * component_diff)
                else:
                    plastic += 0
                plastic_date_lst.append(produce_date)
            if component.required_material.name == "FRP":
                if component_diff > 0:
                    frp += (component.weight * component_diff)
                else:
                    frp += 0
                frp_date_lst.append(produce_date)
            if component.required_material.name == "黑膠傘布" or component.required_material.name == "防潑水傘布":
                fabric += (component.weight * component_diff)
                fabric_q = fabric - Material.objects.get(name=component.required_material.name).inventory
                fabric_date = str(produce_date - timedelta(days=Material.objects.get(name=component.required_material.name).material_detail.lead_time))
            # if component.required_material.name == "防潑水傘布":
            #     fabric += (component.weight * component_diff)
            #     abs_fabric = abs(fabric)
            #     fabric_q = fabric - Material.objects.get(name="防潑水傘布").inventory
            #     fabric_date = str(produce_date - timedelta(days=Material.objects.get(name="防潑水傘布").material_detail.lead_time))
        # plastic = plastic * num 
        # frp = frp * num 
        # fabric = fabric * num
        plastic_q = plastic - Material.objects.get(name="塑膠").inventory
        frp_q = frp - Material.objects.get(name="FRP").inventory
        plastic_date = str(min(plastic_date_lst) - timedelta(days=Material.objects.get(name="塑膠").material_detail.lead_time))
        frp_date = str(min(frp_date_lst) - timedelta(days=Material.objects.get(name="FRP").material_detail.lead_time))
        return render(request, 'modules/inventory/schedule_form.html', locals())

