# Generated by Django 3.1.6 on 2021-02-21 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0017_auto_20210220_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='completionDate',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]