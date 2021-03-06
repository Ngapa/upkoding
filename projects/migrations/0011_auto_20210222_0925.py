# Generated by Django 3.1.6 on 2021-02-22 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20210220_1147'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='project',
            name='slug_idx',
        ),
        migrations.RemoveIndex(
            model_name='project',
            name='is_active_idx',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='userproject',
            name='project_completed',
        ),
        migrations.RemoveField(
            model_name='userproject',
            name='requirements_completed',
        ),
        migrations.AddField(
            model_name='project',
            name='require_demo_url',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='require_sourcecode_url',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Draft'), (1, 'Pending'), (2, 'Active'), (3, 'Deleted')], default=0, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='userproject',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'In Progress'), (1, 'Pending Review'), (2, 'Need Revision'), (3, 'Complete')], default=0, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='userproject',
            name='demo_url',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='URL demo proyek'),
        ),
        migrations.AlterField(
            model_name='userproject',
            name='note',
            field=models.TextField(blank=True, default='', verbose_name='Catatan'),
        ),
        migrations.AlterField(
            model_name='userproject',
            name='sourcecode_url',
            field=models.CharField(blank=True, default='', max_length=250, verbose_name='URL kode sumber proyek'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['slug'], name='project_slug_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['status'], name='project_status_idx'),
        ),
        migrations.AddIndex(
            model_name='userproject',
            index=models.Index(fields=['status'], name='user_project_status_idx'),
        ),
    ]
