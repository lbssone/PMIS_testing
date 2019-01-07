from django.db import models
import math

# Create your models here.        
class Material_detail(models.Model):
    name = models.CharField(max_length=30, null=True)
    year_demand = models.PositiveIntegerField(blank=True, null=True)
    holding_cost = models.PositiveIntegerField(blank=True, null=True)
    ordering_cost = models.PositiveIntegerField(blank=True, null=True)
    usage_rate = models.PositiveIntegerField(blank=True, null=True)
    lead_time = models.PositiveIntegerField(blank=True, null=True)
    eoq = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True, null=True
    )
    rop = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.eoq = math.sqrt(2 * self.year_demand * self.ordering_cost / self.holding_cost)
        self.rop = self.usage_rate * self.lead_time
        super(Material_detail, self).save(*args, **kwargs)        


class Material(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, null=True)
    inventory = models.PositiveIntegerField(blank=True, null=True)
    level =  models.PositiveIntegerField(blank=True, null=True)
    material_detail = models.ForeignKey(Material_detail, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Component_detail(models.Model):
    name = models.CharField(max_length=30, null=True)
    year_demand = models.PositiveIntegerField(blank=True, null=True)
    holding_cost = models.PositiveIntegerField(blank=True, null=True)
    setup_cost = models.PositiveIntegerField(blank=True, null=True)
    produce_rate = models.PositiveIntegerField(blank=True, null=True)
    usage_rate = models.PositiveIntegerField(blank=True, null=True)
    lead_time = models.PositiveIntegerField(blank=True, null=True)
    epq = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.epq = math.sqrt((2 * self.year_demand * self.setup_cost * self.produce_rate) / (self.holding_cost * (self.produce_rate - self.usage_rate)))
        super(Component_detail, self).save(*args, **kwargs)


class Component(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    number_needed = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=30, null=True)
    inventory = models.PositiveIntegerField(blank=True, null=True)
    level =  models.PositiveIntegerField(blank=True, null=True)
    required_material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True)
    weight = models.PositiveIntegerField(blank=True, null=True)
    component_detail = models.ForeignKey(Component_detail, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    number = models.PositiveIntegerField(blank=True, null=True)
    UV = '抗UV'
    WIND = '防風'
    LIGHT = '輕量'
    FEATURE_CHOICES = (
        (UV, '抗UV'),
        (WIND, '防風'),
        (LIGHT, '輕量')
    )
    u_feature = models.CharField(
        max_length=50,
        choices=FEATURE_CHOICES,
        null=True,
    )
    STRAIGHT = '直傘'
    AUTO_F = '自動摺傘'
    MANUAL_F = '手開摺傘'
    TYPE_CHOICES = (
        (STRAIGHT, '直傘'),
        (AUTO_F, '自動摺傘'),
        (MANUAL_F, '手開摺傘')
    )
    u_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        null=True,
    )
    inventory = models.PositiveIntegerField(blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    level =  models.PositiveIntegerField(blank=True, null=True)
    components_required = models.ManyToManyField(Component, blank=True)

    def __str__(self):
        return '{}{}'.format(self.u_feature, self.u_type)

    def getComponents(self):
        return self.components_required.all() 
         
    @property
    def name(self):
        return '{}{}'.format(self.u_feature, self.u_type)
