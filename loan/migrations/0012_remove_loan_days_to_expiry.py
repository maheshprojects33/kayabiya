# Generated by Django 4.2.16 on 2025-05-26 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0011_loan_settled_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='days_to_expiry',
        ),
    ]
