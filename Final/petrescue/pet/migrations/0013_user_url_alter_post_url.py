# Generated by Django 4.0.1 on 2024-02-27 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0012_alter_post_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='url',
            field=models.URLField(blank=True, max_length=600),
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.URLField(blank=True, max_length=600),
        ),
    ]