# Generated by Django 3.2 on 2021-05-01 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='number_of_members',
        ),
    ]
