# Generated by Django 4.2.2 on 2023-06-20 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_collection_updating'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='prompttemplate',
            name='current_template',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='token_size',
        ),
        migrations.RemoveField(
            model_name='chunk',
            name='token_size',
        ),
        migrations.RemoveField(
            model_name='prompttemplate',
            name='template',
        ),
        migrations.RemoveField(
            model_name='question',
            name='token_size',
        ),
        migrations.AddField(
            model_name='prompttemplate',
            name='answer_format',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prompttemplate',
            name='instruction',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prompttemplate',
            name='question_format',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prompttemplate',
            name='separator',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AddConstraint(
            model_name='prompttemplate',
            constraint=models.UniqueConstraint(condition=models.Q(('active', True)), fields=('name',), name='current_template'),
        ),
    ]
