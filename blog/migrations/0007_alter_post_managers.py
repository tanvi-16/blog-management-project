# Generated by Django 5.1.5 on 2025-01-23 07:30

import django.db.models.manager
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_post_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='post',
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
    ]