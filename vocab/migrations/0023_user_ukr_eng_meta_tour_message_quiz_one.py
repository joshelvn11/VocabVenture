# Generated by Django 5.0.2 on 2024-04-14 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0022_user_ukr_eng_meta_tour_message_home_one_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_ukr_eng_meta',
            name='tour_message_quiz_one',
            field=models.BooleanField(default=True),
        ),
    ]