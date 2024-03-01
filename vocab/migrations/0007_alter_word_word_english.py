# Generated by Django 5.0.2 on 2024-03-01 20:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0006_alter_word_word_english'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='word_english',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=['No translation'], size=None),
        ),
    ]
