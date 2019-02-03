# Generated by Django 2.1.3 on 2019-02-03 14:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0002_movies_releasedate'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField(auto_now_add=True)),
                ('profilePic', models.ImageField(blank=True, upload_to='profile_img')),
                ('mobileNumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMovieStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('lastWatchPos', models.DurationField()),
                ('allowRecommend', models.BooleanField(default=True)),
                ('movieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userstats', to='movies.Movies')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moviestats', to='account.User')),
            ],
        ),
    ]