# Generated by Django 4.2.7 on 2023-11-22 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_cpf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adress',
            name='state',
        ),
    ]
