# Generated by Django 5.1.5 on 2025-02-25 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0002_rename_last_nane_profile_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TextField(blank=True)),
                ('message', models.TextField(blank=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_fb.profile')),
            ],
        ),
    ]
