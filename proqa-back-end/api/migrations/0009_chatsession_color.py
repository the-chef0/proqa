# Generated by Django 4.2.2 on 2023-06-08 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_chatsession_pinned'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsession',
            name='color',
            field=models.CharField(default='rgb(1,103,177)', max_length=16),
        ),
    ]