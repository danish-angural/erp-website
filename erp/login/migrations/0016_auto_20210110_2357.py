# Generated by Django 3.1.2 on 2021-01-10 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20210105_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='utype',
            field=models.CharField(default='CUS', max_length=3),
        ),
    ]
