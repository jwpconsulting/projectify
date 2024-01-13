# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2022, 2023 JWP Consulting GK
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
"""User app serializers."""
from typing import (
    Optional,
)

from rest_framework import (
    serializers,
)

from projectify import (
    utils,
)

from . import (
    models,
)


class UserSerializer(serializers.ModelSerializer[models.User]):
    """User serializer."""

    profile_picture = serializers.SerializerMethodField()

    def get_profile_picture(self, obj: models.User) -> Optional[str]:
        """Return profile picture."""
        return utils.crop_image(obj.profile_picture, 100, 100)

    class Meta:
        """Meta."""

        model = models.User
        fields = (
            "email",
            "preferred_name",
            "profile_picture",
        )
