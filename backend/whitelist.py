# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Whitelist for vulture. Not currently used for testing."""
# ruff: noqa: F821
app_name  # unused variable (workspace/urls.py:11)
constraints  # unused variable (workspace/models.py:967)
django_get_or_create  # unused variable (user/factory.py:37)
extra  # unused variable (workspace/admin.py:23)
format  # unused variable (workspace/views/workspace.py:114)
inlines  # unused variable (workspace/admin.py:92)
list_display  # unused variable (workspace/admin.py:93)
list_select_related  # unused variable (workspace/admin.py:99)
lookup_field  # unused variable (blog/views.py:34)
order_with_respect_to  # unused variable (workspace/models.py:966)
ordering  # unused variable (workspace/models.py:1022)
parser_classes  # unused variable (workspace/views/workspace.py:108)
published  # unused variable (blog/models.py:40)
read_only_fields  # unused variable (workspace/serializers/base.py:122)
readonly_fields  # unused variable (workspace/admin.py:37)
serializer_class  # unused variable (workspace/views/workspace.py:90)
unique_together  # unused variable (workspace/models.py:892)
