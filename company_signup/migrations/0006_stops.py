# Generated by Django 4.0.3 on 2022-10-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_signup', '0005_advertisers_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stops',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=1023, null=True)),
                ('longitude', models.CharField(max_length=50, null=True)),
                ('latitude', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]