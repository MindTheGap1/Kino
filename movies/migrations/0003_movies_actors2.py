# Generated by Django 2.1.3 on 2019-02-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movies_releasedate'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='actors2',
            field=models.ManyToManyField(related_name='actors2', to='movies.Actors'),
        ),
    ]
