# Generated by Django 3.0.3 on 2021-01-10 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sih2', '0009_auto_20210110_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default=1, max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='static/images'),
        ),
    ]
