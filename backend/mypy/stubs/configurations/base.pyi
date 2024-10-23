# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import (
    Optional,
)

class ConfigurationBase(type): ...

class Configuration(metaclass=ConfigurationBase):
    DOTENV_LOADED: Optional[str]
    @classmethod
    def load_dotenv(cls) -> None: ...
    @classmethod
    def pre_setup(cls) -> None: ...
    @classmethod
    def post_setup(cls) -> None: ...
    @classmethod
    def setup(cls) -> None: ...
