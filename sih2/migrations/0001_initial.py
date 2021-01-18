# Generated by Django 3.1.5 on 2021-01-18 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200)),
                ('password', models.CharField(default=1, max_length=200)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Farmer_register',
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
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Transport_register',
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
            name='ToDeliver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('agencyname', models.CharField(max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.order')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('agencyname', models.CharField(max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('img', models.ImageField(blank=True, null=True, upload_to='')),
                ('product_type', models.PositiveSmallIntegerField(choices=[(1, 'Food'), (2, 'Cash'), (3, 'Plantation'), (4, 'Horticulture')])),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('farmer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.farmer_register')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('farmer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.farmer_register')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.product')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedDeliveries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=200)),
                ('zipcode', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('agencyname', models.CharField(max_length=200, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sih2.order')),
            ],
        ),
    ]
