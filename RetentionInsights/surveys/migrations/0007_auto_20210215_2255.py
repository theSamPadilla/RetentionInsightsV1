# Generated by Django 3.1.6 on 2021-02-16 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20210215_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_text',
            name='type',
            field=models.CharField(choices=[('S5', 'Slider 0 to 5'), ('Bool', 'Boolean'), ('ST', 'Short Text'), ('LText', 'Long Text')], max_length=20),
        ),
    ]
