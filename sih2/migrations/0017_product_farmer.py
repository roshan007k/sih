# Generated by Django 3.0.3 on 2021-01-17 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sih2', '0016_orderitem_farmer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='farmer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.Farmer_register'),
        ),
    ]
