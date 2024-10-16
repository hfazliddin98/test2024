# Generated by Django 5.1.2 on 2024-10-17 05:05

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mavzular',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('mavzu', models.CharField(max_length=255)),
                ('qrcode', models.ImageField(blank=True, upload_to='mavzu')),
                ('qrlink', models.CharField(blank=True, max_length=255)),
                ('yaratish', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Testlar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('savol', models.CharField(max_length=500)),
                ('variant_a', models.CharField(max_length=255)),
                ('variant_b', models.CharField(max_length=255)),
                ('variant_c', models.CharField(max_length=255)),
                ('variant_d', models.CharField(max_length=255)),
                ('togri_javob', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
                ('mavzu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.mavzular')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Talabas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('fakultet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.fakultets')),
                ('guruh_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.guruhs')),
                ('kurs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.kurs')),
                ('yonalish_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.yonalishs')),
                ('tast_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.testlar')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
