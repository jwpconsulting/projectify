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
"""Projectify base models."""

from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from django_extensions.db.fields import (
    CreationDateTimeField,
    ModificationDateTimeField,
)


class BaseModel(Model):
    """
    The base model to use for all Projectify models.

    This previously used the django-extensions TimeStampedModel. Since only the
    created and modified fields were needed, they were copied here and the save
    override was left out.
    """

    created = CreationDateTimeField(verbose_name=_("created"))
    modified = ModificationDateTimeField(verbose_name=_("modified"))

    class Meta:
        """Make this model abstract."""

        abstract = True
        get_latest_by = "modified"
