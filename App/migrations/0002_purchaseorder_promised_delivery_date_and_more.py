# Generated by Django 4.2.10 on 2024-05-01 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='promised_delivery_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
