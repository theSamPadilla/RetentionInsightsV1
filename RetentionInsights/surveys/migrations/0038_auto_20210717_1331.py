# Generated by Django 3.1.7 on 2021-07-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0037_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fired_p',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='resigned_p',
            field=models.BooleanField(default=False),
        ),
    ]