"""Add title and description."""
# Generated by Django 4.0 on 2021-12-15 07:06

from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    """Migration."""

    dependencies = [
        (
            "workspace",
            "0004_alter_workspace_options_alter_"
            "workspaceboard_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="workspace",
            options={},
        ),
        migrations.AlterModelOptions(
            name="workspaceboard",
            options={},
        ),
        migrations.AddField(
            model_name="workspace",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="description"
            ),
        ),
        migrations.AddField(
            model_name="workspace",
            name="title",
            field=models.CharField(
                default="", max_length=255, verbose_name="title"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="description"
            ),
        ),
        migrations.AddField(
            model_name="workspaceboard",
            name="title",
            field=models.CharField(
                default="", max_length=255, verbose_name="title"
            ),
            preserve_default=False,
        ),
    ]
