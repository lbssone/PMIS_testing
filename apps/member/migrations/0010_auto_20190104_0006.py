# Generated by Django 2.0 on 2019-01-03 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_transaction_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(blank=True, max_length=20)),
                ('target_name', models.CharField(max_length=50, null=True)),
                ('activity_date', models.DateField(null=True)),
                ('target', models.IntegerField(blank=True)),
                ('response', models.IntegerField(blank=True)),
                ('cost', models.IntegerField(blank=True)),
                ('target_members', models.ManyToManyField(blank=True, to='member.Member')),
            ],
            options={
                'ordering': ['-activity_date'],
            },
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
    ]