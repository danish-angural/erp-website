# Generated by Django 3.1.4 on 2020-12-29 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_auto_20201229_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='apprej',
            field=models.CharField(default='approve', max_length=10),
        ),
        migrations.AddField(
            model_name='notifications',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
