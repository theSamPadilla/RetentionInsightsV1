# Generated by Django 3.1.7 on 2021-04-15 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0028_auto_20210315_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='employmentTime',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
    ]
