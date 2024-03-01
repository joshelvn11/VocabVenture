# Generated by Django 5.0.2 on 2024-03-01 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0004_word_word_examples_word_word_explanation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='word_gender',
            field=models.IntegerField(choices=[(0, 'None'), (1, 'Male'), (2, 'Female')], default=0),
        ),
    ]
