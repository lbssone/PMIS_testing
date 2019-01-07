from django.db import models
from apps.member.models import Member

# Create your models here.
class Activity(models.Model):
    activity_name = models.CharField(max_length=20, blank=True)
    target_name = models.CharField(max_length=50, null=True)
    activity_date = models.DateField(null=True)
    target = models.IntegerField(blank=True)
    response = models.IntegerField(blank=True)
    cost = models.IntegerField(blank=True)

    #select more than one member
    target_members = models.ManyToManyField(Member, blank=True)

    def __str__(self):
        return '{}  {}'.format(str(self.activity_date), self.activity_name)

    #獲取率
    def get(self):
        try:
            get = round(self.response / self.target,2)
        except ZeroDivisionError:
            get = 0
        return get
    
    #取得成本
    def efficiency(self):
        try:
            efficiency = round(self.cost / self.response,2)
        except ZeroDivisionError:
            efficiency = 0
        return efficiency
    
    class Meta:
        ordering = ["-activity_date"]
