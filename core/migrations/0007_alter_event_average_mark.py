# Generated by Django 5.0.6 on 2024-05-30 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_stadium_photo_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='average_mark',
            field=models.FloatField(default=0.0),
        ),
    ]
