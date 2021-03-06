# Generated by Django 3.2 on 2021-05-03 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsersData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.EmailField(max_length=254)),
                ('pincode', models.CharField(max_length=6)),
                ('mobile_no', models.CharField(max_length=12)),
                ('min_age_limit', models.CharField(max_length=100)),
                ('district_id', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
