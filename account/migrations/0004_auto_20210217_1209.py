# Generated by Django 3.1.6 on 2021-02-17 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='link', to=settings.AUTH_USER_MODEL),
        ),
    ]