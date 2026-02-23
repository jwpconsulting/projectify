# SPDX-FileCopyrightText: 2012-2023, Jannis Leidel and other contributors.
# SPDX-FileCopyrightText: 2025, UhuruTechnology
#
# SPDX-License-Identifier: BSD-3-Clause
# type: ignore

def pristinemethod(func):
    """
    A decorator for handling pristine settings like callables.

    Use it like this::

        from dj_configurator import Configuration, pristinemethod

        class Develop(Configuration):

            @pristinemethod
            def USER_CHECK(user):
                return user.check_perms()

            GROUP_CHECK = pristinemethod(lambda user: user.has_group_access())

    """
    func.pristine = True
    return staticmethod(func)
