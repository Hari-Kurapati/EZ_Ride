# Generated by Django 4.0.3 on 2022-04-27 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_login', '0006_user_purchase_list_dump'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_purchase_list',
            name='dump',
        ),
    ]