# Generated by Django 3.0.4 on 2020-03-31 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200329_2023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='abstractcardmodel',
            old_name='card',
            new_name='card_id',
        ),
        migrations.RenameField(
            model_name='abstractcardmodel',
            old_name='user',
            new_name='user_id',
        ),
    ]
