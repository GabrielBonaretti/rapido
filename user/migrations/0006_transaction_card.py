# Generated by Django 4.2.7 on 2023-11-28 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_card_due_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='card',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='card', to='user.card'),
        ),
    ]