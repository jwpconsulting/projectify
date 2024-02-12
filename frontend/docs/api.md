# API design (2023-10-03)

Some ideas on null and undefined semantics. Nothing definite or final.

Order of preference

1. Leave out value completely (DRF: `required=False`)
2. Allow setting value to undefined
3. Allow setting value to null

`JSON.stringify` in Firefox:

```
JSON.stringify({hello: undefined})
"{}"
```

For updating objects on the server side this can have different interpretations
but we want to pick one approach.

If there is an optional value in a table, let's say a task's assignee, then
not passing it in a task update should be interpreted as unassigning that user.
(If keeping the assignment was important, you'd be passing the user - 2AM API
logic)

As a matter of fact, we should see it as undesirable to pass null at all! Right
now our task create / update API sees assignee as null equivalent to
unassignment. But it would be much better if leaving out the property in the
first place counted as unassignment.

It's a good habit to pass data as completely as you can. We are talking about
passing in a tasks complete data set (excluding comments/attachments/etc.),
which can't be more than 1-2 kb, optimistically. That's doable. Adding
optional arguments where leaving them out in some cases has different semantics
creates too much ambiguity and makes the developer think twice every time
they call an API.
