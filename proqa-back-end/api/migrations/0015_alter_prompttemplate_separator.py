# Generated by Django 4.2.2 on 2023-06-21 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_remove_prompttemplate_current_template_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prompttemplate',
            name='separator',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
    ]
