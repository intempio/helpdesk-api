# Generated by Django 2.0.5 on 2018-06-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0002_auto_20180606_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(blank=True, choices=[('EOD', 'EOD'), ('Webcast', 'Webcast')], max_length=20),
        ),
    ]