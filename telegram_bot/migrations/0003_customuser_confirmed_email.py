# Generated by Django 5.0.6 on 2024-07-05 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0002_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='confirmed_email',
            field=models.BooleanField(default=False),
        ),
    ]
