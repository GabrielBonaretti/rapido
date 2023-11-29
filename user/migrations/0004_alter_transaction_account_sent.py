# Generated by Django 4.2.7 on 2023-11-27 23:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_transaction_account_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='account_sent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='account_sent', to='user.account'),
        ),
    ]