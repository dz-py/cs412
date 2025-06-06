# Generated by Django 5.1.5 on 2025-04-03 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='apartment_number',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='dob',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='dor',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='first_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='last_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='party_affiliation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='precinct_number',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='street_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='street_number',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v20state',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v21primary',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v21town',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v22general',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='v23town',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='voter_score',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='voter',
            name='zip_code',
            field=models.TextField(),
        ),
    ]
