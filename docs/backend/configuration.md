# Configuring the Projectify backend

We would like to use _django configurations_ by jazzband.

- [Repository](https://github.com/jazzband/django-configurations)
- [Documentation](https://django-configurations.readthedocs.io/en/latest/)

Some other options are

- [Django Classy
  Settings](https://django-classy-settings.readthedocs.io/en/latest/)
- [django-class-settings](https://django-class-settings.readthedocs.io/en/latest/)

But given that jazzband has a good reputation of maintaining packages
long-term, we choose to go with the first option.

## Problems that need solving

### Middleware

Django debug toolbar is in the middleware, always. Even if we launch the Projectify backend in production mode, it is still there. Not only does that slow down the
application, but one can't help but feel anxiety over a _debug_ toolbar
potentially leaking into a production application.

### Failed deploys

Too often, we have settings that break only during production because
environment variable edge cases are not handled neatly. The redis instance unit
on Heroku having a different environment variable depending on whether it is
free or not. If we are able to define data types here, we could potentially
have a static type checker catch these issues.

### Weird module import based inheritance

The way it is right now, we are importing from projectify.settings.base into
each individual settings module. That is sort of like inheritance, but much
less predictable.
