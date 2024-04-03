# Generated by Django 5.0.2 on 2024-04-03 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0016_alter_set_ukr_eng_scores_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_ukr_eng_test_log',
            name='quiz_type',
            field=models.IntegerField(choices=[(0, 'SPELLING'), (1, 'FLASHCARD')], default=0),
        ),
    ]