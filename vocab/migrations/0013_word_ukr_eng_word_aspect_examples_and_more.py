# Generated by Django 5.0.2 on 2024-03-26 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0012_word_ukr_eng_word_definition'),
    ]

    operations = [
        migrations.AddField(
            model_name='word_ukr_eng',
            name='word_aspect_examples',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='word_ukr_eng',
            name='word_conjugation',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='word_ukr_eng',
            name='word_declension',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='word_ukr_eng',
            name='word_part_of_speech',
            field=models.IntegerField(choices=[(0, 'Noun'), (1, 'Verb'), (2, 'Adjective')], default=0),
        ),
    ]
