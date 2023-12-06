# Service layer

We largely model how we write the service layer based on the [Django
Styleguide](https://github.com/HackSoftware/Django-Styleguide).

Some specifications:

## Transactions, Save included

A service method MUST save all changes to the DB, and MUST handle its own
transaction, if an atomic transaction is needed.

## Permissions

Although it is usually called authorization, in the Django world we call it
permission. The method to see if a user has permission to perform an action
is called `has_perm` (if PermissionsMixin is subclasses).

A service layer function MUST perform authorization. This allows ut to keep it
authorization logc in one location. A service layer function MUST perform
authorization with a given `who: User` argument. The `User` class MUST be
importedd from `user/models.py`.

Drawback: This couples our service layer tightly to the User model. Any
checking of service functions must create workspace users with the correct
roles.

## Selectors

Selectors return querysets, lists of model instances or singular Optional model
instances. In the case of a queryset or list return, the selector must be
called

```
<resource_name>_find_by_<most significant filter criterion>
```

For example, to define a function that find all workspace boards in a
workspace, one would name it

```
workspace_board_find_by_workspace
```

The reason we name it find, and not filter, is that filter implies ORM
chainability, whereas we want the user to use a complete selector as much as
possible.
