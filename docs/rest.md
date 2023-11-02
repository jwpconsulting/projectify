# Rest API Design

Yes, yes, we aren't really doing RESTful services here. RESTful is something
with hyperlinks and
[HATEOAS](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5).
We don't have that. And that's OK for now.

For everything that doesn't fit the schema we implement regular RPC style
actions, still in DRF.

## Naming

The four fundamental operations for our resources are

- Create
- Read (Detail and List)
- Update
- Delete

In DRF, they are called Create, Retrieve, Update and Destroy, but we go with
the [more
common](https://en.wikipedia.org/wiki/Create,_read,_update,_and_delete)
terminology.

## URLs

Given a resource, we give assign CRUD operation URLs to it as follows, and
also designate the required HTTP verb:

- Create: `/resource_name/` (POST)
- Read (Detail): `/resource_name/<resource_identifier>` (GET)
- Read (List): `/resource_name/` (GET)
- Update: `/resource_name/<resource_identifier>` (PUT)
- Delete: `/resource_name/<resource_identifier>` (DELETE)

## Updating content

We do not allow partial updates (HTTP PATCH). We want updates to be as complete
as possible. The thought process here is that we will be able to catch
a client having incomplete state earlier, rather than later on finding out
that client and server had a very different idea of what the application state
was.

If a resource has properties that are themselves singular resources (nested
singular resources), we handle updates as follows when handling a JSON PUT
request, such as a picture resource being referred to by a user profile:

- Resource is undefined (JSON property not present): Leave
- Resource is null (JSON property set to `null`): Empty out foreign key in the
  nested resource
- Resource is specified: Replace current foreign key with new resource

What happens to the nested resource with its foreign key set to null is not
specified here. In the case of a Django application this will typically
mean that that nested resource needs to be deleted. In the case of a picture
resource not pointing at a just updated user profile, the picture resource
will get deleted.

If a property is a list, then the semantics are similar:

- Resource is undefined: Leave existing list
- Resource is null: Remove all foreign key relations by previous nested list
  resources to this resource
- Resource is specified: Replace current list of resources with new list of
  resources

What happens to the previously nested list resources is
implementation-specific, as with the singular case.
