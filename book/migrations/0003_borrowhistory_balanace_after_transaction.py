# Generated by Django 5.0 on 2024-01-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_alter_review_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowhistory',
            name='balanace_after_transaction',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
