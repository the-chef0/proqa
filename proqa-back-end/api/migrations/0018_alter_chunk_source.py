# Generated by Django 4.2.2 on 2023-06-26 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_chunk_times_referenced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.source'),
        ),
    ]