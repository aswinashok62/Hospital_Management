# Generated by Django 5.1.6 on 2025-02-25 07:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0004_blogs_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogs',
            name='id_category',
        ),
        migrations.AlterField(
            model_name='blogs',
            name='posted_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
