# Generated by Django 4.2.2 on 2023-07-06 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_llm_batch_size_llm_gpu_layers_llm_temperature'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faqentry',
            options={'verbose_name_plural': 'FAQ Entries'},
        ),
    ]
