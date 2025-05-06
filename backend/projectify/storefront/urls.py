# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2025 JWP Consulting GK
from django.urls import path

from projectify.storefront.views import accessibility

urlpatterns = [
    path("accessibility/", accessibility),
]
