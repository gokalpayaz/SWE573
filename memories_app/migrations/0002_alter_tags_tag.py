# Generated by Django 4.1.7 on 2023-05-06 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memories_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tag',
            field=models.CharField(max_length=20),
        ),
    ]
