# Generated by Django 5.0.4 on 2024-04-13 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balance',
            name='owes_to',
        ),
    ]
