# Service layer

We largely model how we write the service layer based on the [Django
Styleguide](https://github.com/HackSoftware/Django-Styleguide).

Some specifications:

## Transactions, Save included

A service method MUST save all changes to the DB, and MUST handle its own
transaction, if an atomic transaction is needed.
