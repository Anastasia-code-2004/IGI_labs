# Generated by Django 5.0.4 on 2024-05-29 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='purchase_time',
            field=models.DateTimeField(),
        ),
    ]
