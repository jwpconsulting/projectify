# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Whitelist for vulture. Not currently used for testing."""

# ruff: noqa: F821
app_name  # unused variable (workspace/urls.py:11)
django_get_or_create  # unused variable (user/factory.py:37)
format  # unused variable (workspace/views/workspace.py:114)
lookup_field  # unused variable (blog/views.py:34)
parser_classes  # unused variable (workspace/views/workspace.py:108)
serializer_class  # unused variable (workspace/views/workspace.py:90)
# Django models
constraints  # unused variable (workspace/models.py:967)
order_with_respect_to  # unused variable (workspace/models.py:966)
ordering  # unused variable (workspace/models.py:1022)
unique_together  # unused variable (workspace/models.py:892)
# pg triggers
triggers
# Pytest
pytestmark
# DRF serializers
read_only_fields  # unused variable (workspace/serializers/base.py:122)
extra_kwargs  # rest framework
USERNAME_FIELD  # for django auth model override
# Django admin
search_fields
search_help_text
list_filter
extra  # unused variable (workspace/admin.py:23)
inlines  # unused variable (workspace/admin.py:92)
list_display  # unused variable (workspace/admin.py:93)
list_select_related  # unused variable (workspace/admin.py:99)
readonly_fields  # unused variable (workspace/admin.py:37)
