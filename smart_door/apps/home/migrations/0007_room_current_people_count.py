# Generated by Django 4.0.3 on 2022-03-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_room_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='current_people_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
