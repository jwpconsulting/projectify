# SPDX-FileCopyrightText: 2025 JWP Consulting GK
# SPDX-License-Identifier: AGPL-3.0-or-later
from django.core.exceptions import PermissionDenied

class Ratelimited(PermissionDenied): ...
