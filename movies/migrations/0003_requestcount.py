# Generated by Django 3.2.25 on 2024-07-14 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_rename_name_movie_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
