# Generated by Django 4.2.16 on 2024-10-08 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_alter_member_join_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='member',
            old_name='name',
            new_name='username',
        ),
    ]
