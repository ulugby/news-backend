# Generated by Django 5.1.3 on 2024-11-14 19:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_config_telegram_channel_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="config",
            options={
                "verbose_name": "Bot Sozlamasi",
                "verbose_name_plural": "Bot Sozlamalari",
            },
        ),
    ]
