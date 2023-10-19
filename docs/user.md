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

Prefer using AbstractUser over AbstractBaseUser for the return type of a user
generating fixture.
