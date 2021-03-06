# Generated by Django 3.1.6 on 2021-02-18 04:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_project_point'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requirements', models.JSONField(blank=True, null=True, verbose_name='Requirements')),
                ('point', models.IntegerField(default=0)),
                ('demo_url', models.CharField(blank=True, default='', max_length=250)),
                ('sourcecode_url', models.CharField(blank=True, default='', max_length=250)),
                ('note', models.TextField(blank=True, default='')),
                ('requirements_completed', models.BooleanField(default=False)),
                ('project_completed', models.BooleanField(default=False)),
                ('likes_count', models.IntegerField(default=0)),
                ('comments_count', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to='projects.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
