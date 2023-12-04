# Generated by Django 4.2.7 on 2023-12-04 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valueLoan', models.FloatField()),
                ('numberTotalParcels', models.IntegerField()),
                ('numberPayedParcels', models.IntegerField(default=0)),
                ('observation', models.CharField(max_length=255)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='LoanParcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_parcel', models.IntegerField()),
                ('value_parcel', models.FloatField()),
                ('due_date', models.DateField()),
                ('paid', models.BooleanField(default=False)),
                ('paid_date', models.DateField(default=None, null=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='loan.loan')),
            ],
        ),
    ]