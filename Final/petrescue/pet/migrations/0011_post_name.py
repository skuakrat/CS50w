# Generated by Django 4.0.1 on 2024-02-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0010_post_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='name',
            field=models.TextField(blank=True),
        ),
    ]