import json
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, View
from django.db.models import Count, Q
from datetime import datetime, timedelta

from mysite.views import ListView
from .models import Member
from apps.inventory.models import Product

# Create your views here.
class MemberList(View):
    # model = Member
    # template_name = 'modules/member/member.html'
    # context_object_name = 'member_list'
    # base_url = 'member:list'

    def get(self, request):
        dataset = Member.objects \
            .values('dwelling') \
            .annotate(north_count=Count('dwelling', filter=Q(dwelling="北部")),
                    central_count=Count('dwelling', filter=Q(dwelling="中部")),
                    south_count=Count('dwelling', filter=Q(dwelling="南部"))) \
            .order_by('dwelling')

        categories = list()
        north_data = list()
        central_data = list()
        south_data = list()

        for entry in dataset:
            categories.append(entry['dwelling'])
            north_data.append(entry['north_count'])
            central_data.append(entry['central_count'])
            south_data.append(entry['south_count'])

        north = {
            'name': '北部',
            'data': north_data,
            'color': 'green',
        }

        central = {
            'name': '中部',
            'data': central_data,
            'color': 'red',
        }

        south = {
            'name': '南部',
            'data': south_data,
            'color': 'blue',
        }

        chart = {
            'chart': {'type': 'column'},
            'title': {'text': '會員居住地分布'},
            'xAxis': {'categories': categories},
            'series': [north, central, south],
            'plotOptions': {
			    'series': {
        	        'grouping': False,
			    }
		    }
        }


        dump = json.dumps(chart)

        return render(request, 'modules/member/member.html', {'chart': dump})


class MemberSearch(View):
    def get(self, request):
        return render(request, 'modules/member/membersearch.html')

    def post(self, request):
        target_age = self.request.POST.get('target_age')
        target_gender = self.request.POST.get('target_gender')
        target_dwelling = self.request.POST.get('target_dwelling')
        if target_age == 'all':
            members = Member.objects.all()
        else:
            members = Member.objects.filter(age=target_age, gender=target_gender, dwelling=target_dwelling)
        return render(request, 'modules/member/membersearch.html',{'members':members})

class Piechart(View):
    def get(self, request):
        female_count=Member.objects.filter(gender='F').count()
        male_count=Member.objects.filter(gender='M').count()

        seventeen=Member.objects.filter(age='0-17').count()
        thirty=Member.objects.filter(age='18-30').count()
        forty=Member.objects.filter(age='31-40').count()
        fifty=Member.objects.filter(age='41-50').count()
        up=Member.objects.filter(age='51').count()

        north=Member.objects.filter(dwelling='北部').count()
        middle=Member.objects.filter(dwelling='中部').count()
        south=Member.objects.filter(dwelling='南部').count()
        east=Member.objects.filter(dwelling='東部').count()
        other=Member.objects.filter(dwelling='其他').count()

        return render(request, 'modules/member/piechart.html',locals())
