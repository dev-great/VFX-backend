# Generated by Django 3.2.12 on 2022-03-11 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accountsetup', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='payment_for',
            new_name='paymentFor',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='paystack_access_code',
            new_name='paystackAccessCode',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='reference_code',
            new_name='referenceCode',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='expires_in',
        ),
    ]