# Generated by Django 4.0.4 on 2022-05-31 22:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='note_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 2, 1, 24, 38, 694447), verbose_name='Дата и время'),
        ),
    ]
