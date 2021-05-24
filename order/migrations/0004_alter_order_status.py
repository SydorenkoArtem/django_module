# Generated by Django 3.2.3 on 2021-05-23 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20210523_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[[1, 'Created'], [2, 'Canceled'], [3, 'Confirmed'], [4, 'Completed'], [5, 'Rejected']], default='1'),
        ),
    ]