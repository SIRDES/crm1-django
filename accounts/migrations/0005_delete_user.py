# Generated by Django 3.0.6 on 2020-06-10 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0004_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
