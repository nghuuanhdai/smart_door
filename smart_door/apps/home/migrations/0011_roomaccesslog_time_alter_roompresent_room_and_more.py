# Generated by Django 4.0.3 on 2022-04-25 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0010_merge_20220426_0031'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomaccesslog',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='roompresent',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='home.room'),
        ),
        migrations.AlterField(
            model_name='roompresent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='roompresent',
            unique_together={('room', 'user')},
        ),
    ]
