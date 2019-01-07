import json
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, View
from django.db.models import Q

from datetime import datetime, timedelta

from mysite.views import ListView
from .models import Transaction, Transaction_product
from apps.inventory.models import Product

# Create your views here.
class TransactionSeason(View):
    def get(self, request):
        return render(request, 'modules/transaction/transaction_season.html')
    def post(self, request):
        req_year = self.request.POST.get('year')
        req_season = self.request.POST.get('season')
        month_start = 0
        month_end = 0
        if req_season == "春季":
            month_start = 3
            month_end = 5
        elif req_season == "夏季":
            month_start = 6
            month_end = 8
        elif req_season == "秋季":
            month_start = 9
            month_end = 11
        elif req_season == "冬季":
            month_start = 12
            month_end = 2
        uv_s_sold = 0
        uv_auto_sold = 0
        uv_manual_sold = 0
        wind_s_sold = 0
        wind_auto_sold = 0
        wind_manual_sold = 0
        l_s_sold = 0
        l_auto_sold = 0
        l_manual_sold = 0
        if req_season != "冬季":
            products = Transaction_product.objects.filter(transaction__date__year=req_year, transaction__date__month__gte=month_start, transaction__date__month__lte=month_end)
            for trans_data in products:
                if trans_data.product.name == "抗UV直傘":
                    uv_s_sold += trans_data.quantity
                elif trans_data.product.name == "抗UV自動摺傘":
                    uv_auto_sold += trans_data.quantity
                elif trans_data.product.name == "抗UV手開摺傘":
                    uv_manual_sold += trans_data.quantity
                elif trans_data.product.name == "防風直傘":
                    wind_s_sold += trans_data.quantity
                elif trans_data.product.name == "防風自動摺傘":
                    wind_auto_sold += trans_data.quantity
                elif trans_data.product.name == "防風手開摺傘":
                    wind_manual_sold += trans_data.quantity
                elif trans_data.product.name == "輕量直傘":
                    l_s_sold += trans_data.quantity
                elif trans_data.product.name == "輕量自動摺傘":
                    l_auto_sold += trans_data.quantity
                elif trans_data.product.name == "輕量手開摺傘":
                    l_manual_sold += trans_data.quantity
        elif req_season == "冬季":
            for trans_data in Transaction_product.objects.filter(Q(transaction__date__year=req_year) and 
            (Q(transaction__date__month=12) | Q(transaction__date__month=1) | Q(transaction__date__month=2))):
                if trans_data.product.name == "抗UV直傘":
                    uv_s_sold += trans_data.quantity
                elif trans_data.product.name == "抗UV自動摺傘":
                    uv_auto_sold += trans_data.quantity
                elif trans_data.product.name == "抗UV手開摺傘":
                    uv_manual_sold += trans_data.quantity
                elif trans_data.product.name == "防風直傘":
                    wind_s_sold += trans_data.quantity
                elif trans_data.product.name == "防風自動摺傘":
                    wind_auto_sold += trans_data.quantity
                elif trans_data.product.name == "防風手開摺傘":
                    wind_manual_sold += trans_data.quantity
                elif trans_data.product.name == "輕量直傘":
                    l_s_sold += trans_data.quantity
                elif trans_data.product.name == "輕量自動摺傘":
                    l_auto_sold += trans_data.quantity
                elif trans_data.product.name == "輕量手開摺傘":
                    l_manual_sold += trans_data.quantity
        return render(request, 'modules/transaction/transaction_season.html', locals())

class TransactionChart(View):
    def get(self, request):
        return render(request, 'modules/transaction/transaction_chart.html')

    def post(self, request):
        year = int(self.request.POST.get('year'))
        month = int(self.request.POST.get('month'))
        uv_s_sold = 0
        uv_auto_sold = 0
        uv_manual_sold = 0
        wind_s_sold = 0
        wind_auto_sold = 0
        wind_manual_sold = 0
        l_s_sold = 0
        l_auto_sold = 0
        l_manual_sold = 0
        for trans_data in Transaction_product.objects.filter(Q(transaction__date__year=year) and 
        Q(transaction__date__month=month)):
            if trans_data.product.name == "抗UV直傘":
                uv_s_sold += trans_data.quantity
            elif trans_data.product.name == "抗UV自動摺傘":
                uv_auto_sold += trans_data.quantity
            elif trans_data.product.name == "抗UV手開摺傘":
                uv_manual_sold += trans_data.quantity
            elif trans_data.product.name == "防風直傘":
                wind_s_sold += trans_data.quantity
            elif trans_data.product.name == "防風自動摺傘":
                wind_auto_sold += trans_data.quantity
            elif trans_data.product.name == "防風手開摺傘":
                wind_manual_sold += trans_data.quantity
            elif trans_data.product.name == "輕量直傘":
                l_s_sold += trans_data.quantity
            elif trans_data.product.name == "輕量自動摺傘":
                l_auto_sold += trans_data.quantity
            elif trans_data.product.name == "輕量手開摺傘":
                l_manual_sold += trans_data.quantity

        # uv_s = {'name': '抗UV直傘', 'data': [uv_s_sold, 1], 'color': 'green',}
        # uv_au = {'name': '抗UV自動摺傘', 'data': [uv_auto_sold, 2], 'color': 'red',}

        chart = {
            'chart': {'type': 'column', 'colors': 'Array.<Highcharts.ColorString>'},
            'title': {
                'text': str(year) + '年 ' + str(month) + '月雨傘銷售分布',
                'style': {
                    'fontFamily': 'Microsoft JhengHei'
                }
            },
            'xAxis': {'categories': ['抗UV直傘', '抗UV自動摺傘', '抗UV手開摺傘', '防風直傘', '防風自動摺傘','防風手開摺傘',
            '輕量直傘', '輕量自動摺傘', '輕量手開摺傘']},
            # 'series': [uv_s, uv_au],
            'series': [{ 
                'name': '銷售量',
                'data': [
                    {'y': uv_s_sold, 'color': '#058DC7'},
                    {'y': uv_auto_sold, 'color': '#50B432'},
                    {'y': uv_manual_sold, 'color': '#ED561B'},
                    {'y': wind_s_sold, 'color': '#DDDF00'},
                    {'y': wind_auto_sold, 'color': '#24CBE5'},
                    {'y': wind_manual_sold, 'color': '#64E572'},
                    {'y': l_s_sold, 'color': '#FF9655'},
                    {'y': l_auto_sold, 'color': '#FFF263'},
                    {'y': l_manual_sold, 'color': '#6AF9C4'},        
                ]
            }],
            
            'plotOptions': {
                'series': {
                    # 'grouping': False,
                }
            }
        }

        dump = json.dumps(chart)

        return render(request, 'modules/transaction/transaction_chart.html', {'chart': dump})
    

    # def get(self, request):
    #         dataset = Transaction_product.objects \
    #         .values('product') \
    #         .annotate(uv_s=Count('product', filter=Q(product__u_feature='抗UV', product__u_type='直傘')), 
    #         uv_auto=Count('product', filter=Q(product__u_feature='抗UV', product__u_type='手開摺傘')))

    #         categories = list()
    #         straight = list()
    #         auto = list()
            
    #         for entry in dataset:
    #             categories.append(entry['product'])
    #             straight.append(entry['uv_s'])
    #             auto.append(entry['uv_auto'])

    #         s = {
    #             'name': '抗UV直傘',
    #             'data': straight,
    #             'color': 'green',
    #         }

    #         au = {
    #             'name': '抗UV手開摺傘',
    #             'data': auto,
    #             'color': 'red',
    #         }


    #         chart = {
    #             'chart': {'type': 'column'},
    #             'title': {'text': '傘'},
    #             'xAxis': {'categories': categories},
    #             'series': [s, au],
    #             'plotOptions': {
    #                 'series': {
    #                     'grouping': False,
    #                 }
    #             }
    #         }


    #         dump = json.dumps(chart)

    #         return render(request, 'modules/member/member.html', {'chart': dump})
