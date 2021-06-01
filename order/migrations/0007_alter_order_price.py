# Generated by Django 3.2.3 on 2021-05-28 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('order', '0006_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product'),
        ),
    ]
