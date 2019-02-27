# Generated by Django 2.1.3 on 2019-02-27 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteGenres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genreId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersfavourite', to='account.User')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favouritegenres', to='account.User')),
            ],
        ),
    ]
