# Generated by Django 4.2.16 on 2025-05-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0002_loan_days_to_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]
