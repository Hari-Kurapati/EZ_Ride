# Generated by Django 4.0.3 on 2022-04-30 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_signup', '0004_alter_advertisers_company_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisers',
            name='deleted',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]