# Generated by Django 3.0.3 on 2021-01-22 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sih2', '0025_remove_orderitem_farmer'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='farmer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sih2.Farmer_register'),
        ),
    ]