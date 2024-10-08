# Generated by Django 5.1 on 2024-08-23 14:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fundi', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='clubs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Dues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField()),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fundi.club')),
            ],
        ),
    ]
