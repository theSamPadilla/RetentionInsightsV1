# Generated by Django 3.1.6 on 2021-02-19 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0014_auto_20210218_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='completed_p',
            field=models.BooleanField(default=False),
        ),
    ]
