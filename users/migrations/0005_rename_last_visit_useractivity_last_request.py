# Generated by Django 3.2.10 on 2022-01-02 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_user_useractivity_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useractivity',
            old_name='last_visit',
            new_name='last_request',
        ),
    ]
