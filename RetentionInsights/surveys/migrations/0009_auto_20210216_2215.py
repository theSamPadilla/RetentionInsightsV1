# Generated by Django 3.1.6 on 2021-02-17 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0008_auto_20210215_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_text',
            name='type',
            field=models.CharField(choices=[('S6', 'Slider 1 to 6'), ('Bool', 'Boolean'), ('ST', 'Short Text'), ('LT', 'Long Text')], max_length=20),
        ),
    ]
