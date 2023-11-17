# Generated by Django 4.2.7 on 2023-11-16 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_url_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='declared_salary',
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=255)),
                ('uf', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=255)),
                ('neighborhood', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('number', models.IntegerField()),
                ('cep', models.CharField(max_length=8)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_account', models.CharField(max_length=10, unique=True)),
                ('agency', models.CharField(max_length=4)),
                ('balance', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
