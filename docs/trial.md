# Trial mode, and its restrictions

Those who are interested in Projectify should be able to evaluate its
usefulness with a gratis (no cost to the interested person) trial mode, without
the burden of a trial that turns itself into a paid-for subscription
automatically after 30 days -- thus taking money from those who forget to
cancel their subscription.

We would not like to be a burden on those, who in a brief moment of
forgetfulness do not click the right button in an admin panel. (we are all busy
and overwhelmed by the human condition, including the author of this document)

On the other hand, being the operator of a Projectify instance means having to
pay for operation costs. So, we would like everyone to have a small piece of
cake and then everyone can eat, to some degree, that cake.

This is where trial mode comes in! It should make a workspace useful enough to
see whether Projectify is worth using or not. What makes or breaks a product
involves many factors, some of which are the following considerations:

- Is the service provider trustful?
- Is the product useful to me?
- Is the product going to be improved?
- If I have a technical issue, or find a bug, do I have confidence that it will
  be addressed?
- Do I feel comfortable with the UI, and does it cater to my specific needs?
- Do I feel comfortable telling other people in my organization to use this
  tool and do I anticipate that they will feel the same usefulness in it that I
  feel?
- Do I agree with the service provider's and product developer's views,
  especially regarding the product itself?
- If I ever do not want to continue using this product, can I switch away
  easily?

I am sure there are more things to consider. In order to help a prospective
user make a useful decision and be able to answer some of the questions that
they have, we want to give them more than 30 days to come up with a decision on
whether to or not to continue with Projectify. Pressure-based sales tactics are
not cool anyway.

Therefore, the first requirement for our trial mode is that it is __without
time restriction__, but of course without the SLA of a paid-for service
agreement. Naturally, providing a bad service during trial mode is bad business
and we would like to make a great impression to our users here.

Time is of essence in building trust, and we would like to give someone as much
time as needed to see whether Projectify is the thing, or not the thing.

Then, while we can not financially support an endless amount of data stored in
a workspace, we would like to host a limited amount of workspace data. It is
not really the amount of data in bytes that is expensive, but the required
uptime and reliability, data migrations, database upgrades that adds cost to
maintaining a product.

Therefore, the next requirement for our trial mode is that there will be a
limit on how many objects can be created as part of a workspace. The
limitations are as follows:

- A user can create as many trial workspaces as they would like
- A trial workspace can have 2 workspace users at most, including the
  creator/owner of the workspace. This also includes open invites. (i.e., sum
  invite
  + user <= 2)
- A trial workspace can hold 10 workspace boards
- A trial workspace can hold 100 sections in total, with no
  per-workspace board limitations
- A trial workspace can hold 1000 tasks. Again, there is no limitation where
  those tasks can be put, they could all be in the same workspace board or
  section.
- A trial workspace can hold 10 labels
- A trial workspace can not have any chat messages (they are not supported by
  the application right now)
- Within a trial workspace, any label can be assigned to any task.
- Within a trial workspace, there can be up to 1000 sub tasks.

There are no limitations for reading, updating and deleting.

# Implementation of workspace trial mode

The most important thing is to ensure that the backend rules implement the
above trial restrictions. Then, we have to show to the user in the frontend
how many more objects of each resource they can create. We can combine this
into a quota API, or as an enhancement to the existing `/workspace/<uuid>/`
GET and also the WebSocket result for a WebSocket subscription.

One can imagine structured data coming back like so, for a workspace object:

```js
{
  "uuid": "workspace-uuid",
  "quota": {
    "workspace_boards": {
      "current": 5,
      "limit": 10
    },
    // and so on
  },
  // other workspace serializer fields
}
```
