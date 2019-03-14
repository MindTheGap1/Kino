# Generated by Django 2.1.3 on 2019-03-14 11:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteGenres',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genreId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usersfavourite', to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(auto_now_add=True)),
                ('profilePic', models.ImageField(blank=True, upload_to='profile_img')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMovieStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('lastWatchPos', models.DurationField(blank=True, null=True)),
                ('recommendValue', models.DecimalField(blank=True, decimal_places=2, default=None, max_digits=4, null=True, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('allowRecommend', models.BooleanField(default=True)),
                ('movieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userstats', to='movies.Movie')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moviestats', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='favouritegenres',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favouritegenres', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='favouritegenres',
            unique_together={('userId', 'genreId')},
        ),
    ]
