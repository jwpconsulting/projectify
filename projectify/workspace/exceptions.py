# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Contain exceptions used in workspace application."""


class UserAlreadyAdded(ValueError):
    """Tell the caller that a user has already been added to a workspace."""


class UserAlreadyInvited(ValueError):
    """Tell the caller that user has already been invited to a workspace."""
