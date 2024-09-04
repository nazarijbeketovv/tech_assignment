# Generated by Django 5.1.1 on 2024-09-04 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Boost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boost_type', models.CharField(choices=[('speed', 'Ускорение'), ('strength', 'Сила'), ('defense', 'Защита')], max_length=20, verbose_name='Тип буста')),
                ('duration', models.DurationField(verbose_name='Длительность буста')),
                ('activated_at', models.DateTimeField(auto_now_add=True, verbose_name='Время активации')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boosts', to='task_1.player')),
            ],
        ),
    ]
