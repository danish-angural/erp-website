# Generated by Django 3.1.4 on 2021-01-08 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20210105_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='optfield1',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='optfield2',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='optfield3',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='optfield4',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
