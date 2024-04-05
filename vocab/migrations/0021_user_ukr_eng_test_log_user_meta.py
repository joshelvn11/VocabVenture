# Generated by Django 5.0.2 on 2024-04-05 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vocab', '0020_remove_user_ukr_eng_test_log_user_meta'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_ukr_eng_test_log',
            name='user_meta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_ukr_eng_meta', to='vocab.user_ukr_eng_meta'),
            preserve_default=False,
        ),
    ]
