<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# User account management

User account models are stored in user/models.py.

## Foreign key to User

There's nothing wrong with coupling!

Implement a foreign key pointing at a user like so:

```python
from projectify.user.models import User

class MyModel(models.Model):
    user = models.ForeignKey["User"](User, on_delete=models.CASCADE)
```

## Testing

Prefer using `projectify.user.models.User` over Django's
`AbstractBaseUser` or `AbstractUser` in test cases and fixtures.
