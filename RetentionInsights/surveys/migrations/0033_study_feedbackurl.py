# Generated by Django 3.1.7 on 2021-04-24 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0032_auto_20210420_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='feedbackUrl',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
    ]
