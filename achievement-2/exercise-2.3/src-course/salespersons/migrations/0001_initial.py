# Generated by Django 4.2.9 on 2024-01-31 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SalesPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=120)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.TextField()),
            ],
        ),
    ]