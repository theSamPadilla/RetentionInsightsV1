# Generated by Django 3.1.6 on 2021-02-17 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0010_auto_20210217_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
