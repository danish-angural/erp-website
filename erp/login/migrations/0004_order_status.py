# Generated by Django 3.1.2 on 2020-12-20 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(default='all approval pending', max_length=100),
        ),
    ]
