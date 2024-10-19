# Generated by Django 5.1.2 on 2024-10-18 16:20

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_rename_mavzular_mavzus_rename_testlar_tests'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Natijas',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('talaba', models.CharField(max_length=255)),
                ('togri', models.IntegerField(default=0)),
                ('notogri', models.IntegerField(default=0)),
                ('fakultet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.fakultets')),
                ('guruh_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.guruhs')),
                ('kurs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.kurs')),
                ('mavzu_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.mavzus')),
                ('yonalish_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.yonalishs')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
