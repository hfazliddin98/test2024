# Generated by Django 5.1.2 on 2024-10-17 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Mavzular',
            new_name='Mavzus',
        ),
        migrations.RenameModel(
            old_name='Testlar',
            new_name='Tests',
        ),
    ]
