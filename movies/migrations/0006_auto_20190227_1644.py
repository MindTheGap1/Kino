# Generated by Django 2.1.3 on 2019-02-27 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20190227_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='length',
            field=models.DurationField(null=True),
        ),
    ]
