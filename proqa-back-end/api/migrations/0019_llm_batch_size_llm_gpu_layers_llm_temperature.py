# Generated by Django 4.2.2 on 2023-07-06 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_chunk_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='llm',
            name='batch_size',
            field=models.PositiveIntegerField(default=1024),
        ),
        migrations.AddField(
            model_name='llm',
            name='gpu_layers',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='llm',
            name='temperature',
            field=models.FloatField(default=0.8),
        ),
    ]
