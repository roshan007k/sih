# Generated by Django 3.0.3 on 2020-12-05 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sih2', '0004_transport_register'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport_register',
            name='transportaadhar',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='transport_register',
            name='transportcode',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='transport_register',
            name='transportcontact',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='transport_register',
            name='transportgst',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='transport_register',
            name='transporttruck',
            field=models.BigIntegerField(),
        ),
    ]
