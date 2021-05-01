# Generated by Django 3.2 on 2021-05-01 23:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Friends', 'Friends')], default=django.utils.timezone.now, max_length=15),
            preserve_default=False,
        ),
    ]
