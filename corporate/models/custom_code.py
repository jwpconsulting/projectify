"""
Custom code model.

Custom codes are used to help beta testers and other interested users sign
up for the Projectify application.

Sign up life cycle

1. Admin creates a custom code
2. Send custom code to user, including instructions on how to use it.
3. User signs up on Projectify, creates Workspace during onboarding
4. User goes to workspace billing settings and enters custom code.
5. Custom plan is unlocked for this workspace, with the available seats set
to the sign up code seats.
6. Custom code is marked as used and cannot be reused.

A custom code does not:

- Have an expiry date by which it needs to be used (for now at least)
- Assign an expiring plan to a customer. Seats will be available indefinitely
(for now at least)
- Constitute what we want to use for campaign or coupon codes in the future,
in order to offer rebates and special offers


State transitions viewed from CustomCode

        User enters sign up code
           │
           │
   ┌─────┐ │   ┌──────┐       ┌─────────────┐
   │ New ├─┴──►│ Used ├──┬───►│ No customer │
   └─────┘     └──────┘  │    └─────────────┘
                         │
                         │
                         │
                         │
                      Workspace/Customer deleted


State transitions viewed from Customer


                    Create                         Re-subscribe
                    subscription
             ┌───────────────────────────────┐ ┌───────────────┐
             │                               │ │               │
             │                               ▼ ▼               │
          ┌──┴───┐       ┌──────┐        ┌──────┐          ┌─────────┐
─────────►│Unpaid├──────►│Custom├───────►│Active│────────► │Cancelled│
Create    └──────┘Enter  └──────┘ Create └──────┘ Subscr.  └─────────┘
workspace         custom     ▲    subscription│   expires or     │
and               code       │                │   is cancelled   │
customer                     └────────────────┘                  │
                             ▲  Enter                            │
                             │  custom                           │
                             │  code                             │
                             └───────────────────────────────────┘

"""
from django.db import models

from projectify.lib.models import BaseModel

from .customer import Customer


class CustomCode(BaseModel):
    """
    Store information about a custom code.

    The code can be used up by updating "used" with the current timestamp,
    and setting customer.

    NOTE: a deleted customer will set "customer" back to null, but it does not
    mean that this sign up code has not been used.

    The idea is that we want to avoid re-using custom codes after a related
    customer has been deleted. We want to keep a permanent record of all custom
    codes ever created. Deleting a custom code will make it difficult to keep
    a record.

    A custom code stores how many seats will be unlocked for a customer, when
    it is used for that customer.

    A custom code MUST not be usable twice, even for the same customer.
    """

    code = models.CharField(max_length=200, unique=True, db_index=True)

    customer = models.ForeignKey[Customer](
        Customer, null=True, editable=False, on_delete=models.SET_NULL
    )
    used = models.DateTimeField(editable=False, blank=True, null=True)

    seats = models.PositiveIntegerField()
