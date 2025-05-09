<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# User account management

User account models are stored in user/models.py.

## Foreign key to user

Implement a foreign key pointing at a user like so:

```python
from django.contrib.auth.models import (
    AbstractUser,
)

class MyModel(models.Model):
    user = models.ForeignKey["AbstractUser"](
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
)
```

## Testing

Prefer using User over AbstractBaseUser or AbstractUser.
