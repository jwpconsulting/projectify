"""User signals."""
from django import (
    dispatch,
)


user_invitation_redeemed = dispatch.Signal()
