# Generated by Django 5.0.6 on 2024-05-20 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_stadium_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadium',
            name='photo_link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
