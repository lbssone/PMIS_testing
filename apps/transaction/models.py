from django.db import models
from apps.member.models import Member
from apps.inventory.models import Product

# Create your models here.
class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    products = models.ManyToManyField(Product, through='Transaction_product')

    def __str__(self):
        return '{} {}'.format(self.member.member_name, str(self.date))

    @staticmethod
    def calculate_total_price(self):
        t_price = 0
        for tran in self.transaction_product_set.all():
            t_price += tran.price
        return t_price
        # return self.product.all().aggregate(total_price=Sum('price'))['total_price']

    def save(self, *args, **kwargs):
        try:
            self.total_price = Transaction.calculate_total_price(self)
        except:
            self.total_price = 0
        super(Transaction, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-date"] 

class Transaction_product(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.transaction.member.member_name + " " + str(self.transaction.date)
    
    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super(Transaction_product, self).save(*args, **kwargs)
    
    @property
    def date(self):
        return str(self.transaction.date)
