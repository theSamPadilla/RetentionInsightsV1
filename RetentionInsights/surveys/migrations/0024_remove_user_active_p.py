# Generated by Django 3.1.6 on 2021-03-02 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0023_auto_20210301_1542'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active_p',
        ),
    ]
