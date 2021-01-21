# Generated by Django 3.0.3 on 2021-01-20 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sih2', '0018_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Farmer_notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agencyname', models.CharField(max_length=100)),
                ('transportname1', models.CharField(max_length=100)),
                ('transportname2', models.CharField(max_length=100)),
                ('transportpassword', models.CharField(max_length=50)),
                ('transportcost', models.BigIntegerField()),
                ('transporttruck', models.BigIntegerField()),
                ('transportcontact', models.BigIntegerField()),
                ('transportaddress', models.CharField(max_length=200)),
                ('transportaddress1', models.CharField(max_length=200)),
                ('transportstate', models.CharField(max_length=50)),
                ('transportdistrict', models.CharField(max_length=50)),
                ('transporttaluka', models.CharField(max_length=50)),
                ('transportcity', models.CharField(max_length=50)),
                ('transportcode', models.BigIntegerField()),
                ('transportaadhar', models.BigIntegerField()),
                ('transportgst', models.BigIntegerField()),
                ('aadhar', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Transport_notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('confirmpassword', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_number', models.CharField(max_length=100, unique=True)),
                ('address', models.TextField(max_length=200)),
                ('address1', models.TextField(blank=True, max_length=200)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('taluka', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Buyer_notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.Customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.Order')),
            ],
        ),
    ]
