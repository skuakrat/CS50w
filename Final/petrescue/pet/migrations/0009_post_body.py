# Generated by Django 4.0.1 on 2024-02-15 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0008_post_address_post_province_delete_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='body',
            field=models.TextField(blank=True),
        ),
    ]
