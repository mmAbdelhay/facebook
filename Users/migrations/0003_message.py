# Generated by Django 3.2 on 2021-04-30 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Users', '0002_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.DateField(auto_now_add=True)),
                ('content', models.TextField(max_length=1024)),
                ('receiverID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('senderID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('senderID', 'receiverID', 'Time')},
            },
        ),
    ]