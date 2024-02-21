# Generated by Django 5.0.2 on 2024-02-15 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='превью')),
            ],
            options={
                'verbose_name': 'курс',
                'verbose_name_plural': 'курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='превью')),
                ('video_link', models.URLField(blank=True, null=True, verbose_name='ссылка на видео')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.course', verbose_name='курс')),
            ],
            options={
                'verbose_name': 'урок',
                'verbose_name_plural': 'уроки',
            },
        ),
    ]