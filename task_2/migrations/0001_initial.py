# Generated by Django 5.1.1 on 2024-09-05 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.DateField()),
                ('is_completed', models.BooleanField(default=False)),
                ('score', models.PositiveIntegerField(default=0)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_2.level')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_2.player')),
            ],
        ),
        migrations.CreateModel(
            name='LevelPrize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received', models.DateField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_2.level')),
                ('prize', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task_2.prize')),
            ],
        ),
    ]
