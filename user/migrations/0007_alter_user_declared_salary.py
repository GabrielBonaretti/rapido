# Generated by Django 4.2.7 on 2023-11-17 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_transaction_type_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='declared_salary',
            field=models.FloatField(default=0, null=True),
        ),
    ]