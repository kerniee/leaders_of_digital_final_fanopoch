# Generated by Django 3.1.3 on 2020-11-28 13:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups_manager', '0006_1_0_0_default'),
        ('main', '0007_auto_20201128_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='to_groups',
            field=models.ManyToManyField(blank=True, related_name='assigned_cards', related_query_name='assigned_card', to='groups_manager.Group', verbose_name='Группам'),
        ),
        migrations.AlterField(
            model_name='card',
            name='to_users',
            field=models.ManyToManyField(blank=True, related_name='assigned_cards', related_query_name='assigned_card', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ConjunctiveGroup',
        ),
    ]
