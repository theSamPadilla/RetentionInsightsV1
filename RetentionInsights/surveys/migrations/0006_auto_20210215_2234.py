# Generated by Django 3.1.6 on 2021-02-16 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0005_auto_20210215_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question_text',
            old_name='questionType',
            new_name='type',
        ),
    ]
