# Generated by Django 5.1.2 on 2024-10-26 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_fakultets_options_alter_guruhs_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guruhs',
            name='name',
            field=models.CharField(default='1-guruh', max_length=255),
        ),
        migrations.AlterField(
            model_name='kurs',
            name='name',
            field=models.CharField(default='1-kurs', max_length=255),
        ),
    ]