# Generated by Django 5.2.3 on 2025-06-27 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0009_alter_installedplugin_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InstalledPlugin',
        ),
    ]
