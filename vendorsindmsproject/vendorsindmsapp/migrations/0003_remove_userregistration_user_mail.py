# Generated by Django 3.0.4 on 2020-03-14 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendorsindmsapp', '0002_auto_20200314_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistration',
            name='user_mail',
        ),
    ]
