# Generated by Django 4.0.3 on 2022-03-20 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_schedule_schedule_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
