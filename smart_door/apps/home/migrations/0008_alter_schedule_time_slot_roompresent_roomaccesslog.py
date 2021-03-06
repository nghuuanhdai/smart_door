# Generated by Django 4.0.3 on 2022-03-31 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_room_current_people_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time_slot',
            field=models.PositiveSmallIntegerField(default=9),
        ),
        migrations.CreateModel(
            name='RoomPresent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.FloatField(default=37)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomAccessLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.FloatField(default=37)),
                ('status', models.TextField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
