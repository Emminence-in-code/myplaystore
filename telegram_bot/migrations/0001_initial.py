# Generated by Django 5.0.6 on 2024-07-04 10:32

import django.db.models.deletion
import telegram_bot.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('full_name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='UploadedApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('company_name', models.CharField(max_length=200)),
                ('app_name', models.CharField(max_length=200)),
                ('platform', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('version', models.CharField(max_length=200)),
                ('estimated_size', models.CharField(max_length=200)),
                ('image1', models.ImageField(upload_to=telegram_bot.models.user_directory_path)),
                ('image2', models.ImageField(blank=True, null=True, upload_to=telegram_bot.models.user_directory_path)),
                ('image3', models.ImageField(blank=True, null=True, upload_to=telegram_bot.models.user_directory_path)),
                ('app', models.FileField(upload_to=telegram_bot.models.user_directory_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='telegram_bot.customuser')),
            ],
        ),
    ]