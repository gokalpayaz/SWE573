# Generated by Django 4.1.7 on 2023-05-08 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memories_app', '0002_alter_tags_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='date',
            name='exact_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
