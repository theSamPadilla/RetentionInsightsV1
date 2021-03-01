# Generated by Django 3.1.6 on 2021-02-21 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0015_auto_20210219_0046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='survey',
            options={'get_latest_by': 'date'},
        ),
        migrations.AddField(
            model_name='survey',
            name='completionDate',
            field=models.DateTimeField(null=True),
        ),
    ]