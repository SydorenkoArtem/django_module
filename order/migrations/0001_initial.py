# Generated by Django 3.2.3 on 2021-05-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created_at', models.DateField(auto_created=True)),
                ('oid', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(1, 'open'), (2, 'in process'), (3, 'complete')], default=1)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
    ]