# Generated by Django 2.1.3 on 2019-03-18 20:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderId', models.AutoField(primary_key=True, serialize=False)),
                ('paid', models.BooleanField(default=False)),
                ('card_number', models.CharField(max_length=16)),
                ('cardholder_name', models.CharField(max_length=200)),
                ('expiry_date', models.CharField(max_length=7)),
                ('CVV_code', models.CharField(max_length=3)),
                ('orderCreated', models.DateTimeField(auto_now_add=True)),
                ('orderUpdated', models.DateTimeField(auto_now=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=20)),
                ('movieStartTime', models.DateTimeField(blank=True, null=True)),
                ('movieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='movies.Movie')),
                ('orderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movies', to='orders.Order')),
            ],
        ),
    ]