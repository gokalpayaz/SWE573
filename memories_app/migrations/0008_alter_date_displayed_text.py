# Generated by Django 4.1.7 on 2023-05-16 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memories_app', '0007_alter_date_displayed_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='displayed_text',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
