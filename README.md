<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Projectify

Projectify is a free software project management software that anyone can use,
inspect, customize and distribute according to their needs.

Official instance:
[https://www.projectifyapp.com](https://www.projectifyapp.com).

# Development Requirements

- Python version >= 3.12.12 (I recommend using [asdf](https://asdf-vm.com/))
- [poetry](https://python-poetry.org/docs/)
- [PostgreSQL](https://www.postgresql.org/) >= 15.5
- [Node.js](https://nodejs.org/en/download) >= 24.13.1

[Here's how to install asdf](https://asdf-vm.com/guide/getting-started.html)
on your computer.

## Installing Python 3.12 and Node.js 24

Managing Python and Node.js versions is convenient using [asdf](https://asdf-vm.com/):

```bash
asdf plugin-add python
asdf plugin add nodejs https://github.com/asdf-vm/asdf-nodejs.git
asdf install python 3.12.12
asdf install node.js 24.13.1
```

## Installing PostgreSQL 15

Projectify uses PostgreSQL 15. Here's how to install it:

- On **macOS** (using Homebrew): `brew install postgresql@15` [^brew-postgres]
- On **Debian**: `sudo apt install postgresql-15 libpq-dev`
- On **other systems**: See the [PostgresSQL documentation](https://www.postgresql.org/download/)

[^brew-postgres]: [postgresql@15 on *brew.sh*](https://formulae.brew.sh/formula/postgresql@15#default)


Check whether you can connect to your local PostgreSQL instance by using the
following command:

```bash
psql
```

If you've installed PostgreSQL correctly, you should see the following prompt:

```bash
psql (15.14)
Type "help" for help.

debian=#
```

Press `Ctrl+d` to exit `psql`.

# Quickstart

After making sure that you've added the dependencies, follow these
steps to start developing with Projectify:

1. Clone [this repository](https://github.com/jwpconsulting/projectify).
2. Install all dependencies using the Python `poetry` tool.
3. Create a `.env` environment file by copying the `.env.template` file.
4. Edit the `DATABASE_URL` variable in the `.env` file and point it to your
   local PostgreSQL 15 instance.
5. Create a `projectify` PostgreSQL database inside your local PostgreSQL 15
   instance using the `createdb` command.
6. Then, inside a `poetry` shell, perform the following:
  a. Migrate the `projectify` database that you have just created.
  b. Seed the `projectify` database with test data using the `seeddb` command.
  c. Start the development server.
  d. Install the Django-Tailwind[^django-tailwind] tool dependencies.
  e. Start the Django-Tailwind tool.

[^django-tailwind]: [Django-Tailwind](https://django-tailwind.readthedocs.io/en/latest/installation.html) *django-tailwind.readthedocs.io*

Run these shell commands to accomplish the steps 1. to 5.:

```bash
# Clone the repository
git clone git@github.com:jwpconsulting/projectify.git
# Install dependencies
poetry install --with dev --with test --no-root
# Create your `.env` file
cp .env.template .env
# Edit the `.env` file using your preferred editor:
vim .env
# Inside .env, edit the DATABASE_URL, then save your changes.
# Create the database using the PostgreSQL `createdb` command
createdb projectify
```

Possible values for `DATABASE_URL`:

- Connect via `localhost`: `DATABASE_URL=postgres://$USER@localhost/projectify`
  where `$USER` is your username.
- Connect to UNIX domain socket on **Debian**:
  `DATABASE_URL=postgres://%2Fvar%2Flib%2Fpostgresql/projectify`
- Connect to UNIX domain socket on **macOS**:
  `DATABASE_URL=postgres://%2Ftmp/projectify`

To finish with step 6., configure Projectify and run using the following commands:

```bash
# Run the Django migration command
poetry run ./manage.py migrate
# Seed the database with test data using `seeddb`
poetry run ./manage.py seeddb
# Start the development server
poetry run ./manage.py runserver
# Open a new terminal and navigate to the repository again
# Install the tailwind development tool dependencies
poetry run ./manage tailwind install
# Run the tailwind development tool
poetry run ./manage tailwind start
```

Once you have done all of this, go to Django administration page at
<http://localhost:8000/admin/>. The `seeddb` command created an administrator
account with the following credentials for you:

- Username: `admin@localhost`
- Password: `password`

Log in using these credentials and you have full access to the administration
page.

## Neovim

You can use Neovim with the [Pyright](https://github.com/microsoft/pyright) Language Server Protococol (LSP) server. To make sure that Neovim uses the right Pyright from
this repository, run neovim inside a poetry environment like so:

```
poetry run nvim
```

# Formatting
```
poetry run bin/format.sh
```

# Copyright and licencing information
To look for files missing copyright and licencing information:

```
# Assume you are in backend directory
poetry run reuse lint
```

# Nix

You can use the included `flake.nix` Flake file to open a Nix Flake shell
with all development dependencies:

1. Download Nix: <https://nixos.org/download/> (skip if you use NixOS)
2. Enable Nix Flakes: <https://wiki.nixos.org/wiki/Flakes#Enabling_flakes_permanently>
3. Open a Nix Flake shell by running `nix shell` in your terminal

Alternatively, configure [direnv](https://direnv.net/) and [nix-direnv](https://github.com/nix-community/nix-direnv) to automatically jump into a Nix flake shell.

# Translations

Projectify uses Django's built-in GNU gettext-based translation. Learn more
about Django's translation features [here](https://docs.djangoproject.com/en/5.1/topics/i18n/translation/#translate-template-tag).

You can update the translation files by running the following commands:

```bash
./manage.py makemessages --ignore=bin/ -l en --ignore='gunicorn.conf.py' --ignore=manage.py
```

# License

Projectify is licensed under the GNU Affero General Public
License Version 3 or later. Some third party dependencies are vendored in and
available under their respective licenses. Please review the license files
contained in the `LICENSES` directory located in the Projectify repository.

See `AUTHORS.txt` file for the list of contributors.

Projectify is a registered trademark by [JWP Consulting
GK](https://www.jwpconsulting.net).
