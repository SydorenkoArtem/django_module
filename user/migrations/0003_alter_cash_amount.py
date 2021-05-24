# Generated by Django 3.2.3 on 2021-05-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_cash_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cash',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=100000, max_digits=10),
        ),
    ]
