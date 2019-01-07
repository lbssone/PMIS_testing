from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from datetime import datetime, timedelta
from .models import Activity
# Create your views here.

class ActivityDetail(View):
    def get(self, request):
        activities = Activity.objects.all()
        return render(request, 'modules/activity/activity_detail.html', locals())