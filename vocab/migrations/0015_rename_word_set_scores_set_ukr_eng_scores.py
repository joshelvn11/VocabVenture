# Generated by Django 5.0.2 on 2024-03-28 15:19

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0014_word_set_scores_word_ukr_eng_scores'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WORD_SET_SCORES',
            new_name='SET_UKR_ENG_SCORES',
        ),
    ]
