# Generated by Django 3.1.4 on 2020-12-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_order_sales'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='net_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='unit',
            field=models.CharField(default='m', max_length=10),
        ),
        migrations.AddField(
            model_name='order',
            name='unit_price',
            field=models.IntegerField(default=0),
        ),
    ]
