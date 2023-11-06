I am documenting some ideas here on how to serve media files without relying on
3rd parties.

Let's say our application runs on a server and all the user uploaded media
files are in a folder called `/srv/media`.

When a logged in user, let's call them $USER, retrieves their profile
information using the `/user/user` endpoint, they will first receive a (JSON)
response, that will look something like this:

```json { "profile_picture":
"https://api.projectifyapp.com/media/link/to/picture.webp" } ```

This URL points at an endpoint provided by
[django-downloadview](https://github.com/jazzband/django-downloadview).

With django-downloadview we have support for permission checking, so we can
make sure that a user is allowed to retrieve a picture at a specific media
path. This way we can avoid people accessing random S3 bucket-like URLs despite
being logged / removed from an org / etc. [Broken Access Control]
(https://owasp.org/Top10/A01_2021-Broken_Access_Control/) is a problem, yo.

Then, using the streaming optimization setting [included in
django-downloadview](https://django-downloadview.readthedocs.io/en/latest/optimizations/index.html),
we can have the application server tell the web server to handle the request,
and serve a file.

The way this works is as follows

0. The user requests a media file.
1. The web server forwards a request to the application server for a media file
2. The application server verifies that the request is legitimate, and returns
   a response containing a header containing information about where the file
   is stored back to the web server
3. The web server recognizes this special header in the response, combined with
   a agreed upon status code. It then sends out the file pointed to by the path
   in the header.
4. The user receives the requested media file.

More specifically, if we plan to use caddy, we can implement it using the
`handle_response` directive. Some documentation links are as follows:

- [Caddy json config docs on
  handle-response](hhttps://caddyserver.com/docs/json/apps/http/servers/routes/handle/reverse_proxy/handle_response/)
- [Pull request that added this
  functionality](https://github.com/caddyserver/caddy/pull/4021)
- [Issue in caddy that asked for this
  functionality](https://github.com/caddyserver/caddy/issues/3828)

We check the current caddy version in Debian 12:

``` Package: caddy Version: 2.6.2-5 ```

Cloning the [git repo](https://github.com/caddyserver/caddy) we can easily see
that the merge commit is part of 2.6.2-5:

``` $git log v2.6.2 | grep "#3710" reverseproxy: Add `handle_response` blocks
to `reverse_proxy` (#3710) (#4021)
    * reverseproxy: Add `handle_response` blocks to `reverse_proxy` (#3710)
      reverseproxy: Add `buffer_requests` option to `reverse_proxy` directive
      (#3710) ```

Looks good!

# Benefits

Web server does not need to understand user authentication or authorization.

Application can be deployed more easily.

No costly dependency on third party, not exposed to deprecated APIs.

Projectify becomes easy to test, even when testing close to production in a
local environment.

# Challenges

We should ensure that path traversal is impossible. This should be fine as
long as the application server only outputs valid header responses.

Not using cloudinary means that we have to resize and convert images ourselves.
