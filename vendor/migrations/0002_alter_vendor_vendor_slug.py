# Generated by Django 4.2.6 on 2023-10-23 17:29

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='vendor_name', unique=True),
        ),
    ]
