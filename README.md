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

- Python version at least 3.12.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
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

# Quickstart

After making sure that you've added the dependencies, follow these
steps to start developing with Projectify. With these steps, SQLite works out
of the box and no database setup is needed.

1. Clone [this repository](https://github.com/jwpconsulting/projectify):
  ```bash
  git clone git@github.com:jwpconsulting/projectify.git
  ```
2. Install all Python and Node dependencies:
  ```bash
  uv sync --all-groups && npm ci
  ```
3. Create a `.env` environment file by copying the `.env.template` file.
  ```bash
  cp .env.template .env
  ```
4. Prepare the database:
  ```bash
  # Run the Django migration command
  uv run ./manage.py migrate
  # Seed the database with test data and users. Log in with
  # user: admin@localhost
  # password: password
  uv run ./manage.py seeddb
  ```
5. Start the Django development server and Tailwind CSS:
  ```bash
  # Start the development server at http://localhost:8000
  uv run ./manage.py runserver
  # `runserver blocks`, so run the Tailwind CSS development tool
  # in a separate terminal:
  npm start
  ```

Once you have done all of this, go to Django administration page at
<http://localhost:8000/admin/>. The `seeddb` command created an administrator
account with the following credentials for you:

- Username: `admin@localhost`
- Password: `password`

Log in using these credentials and you have full access to the administration
page.

You're done!

# uv

Here's how to update a specific package. Let's say you want to update the
PyJWT package because of a vulnerability report (CVE-2026-32597). Run
the following `uv` command to update the PyJWT version used in Projectiy:

```
uv lock -P pyjwt
```

You should see something like the following:

```
Resolved 114 packages in 491ms
Updated pyjwt v2.11.0 -> v2.12.1
```

Make sure to run `bin/update-requirements` afterwards. Updating PyJWT to
version 2.12.1 results in the following diff for the `requirements.txt` file:

```patch
-pyjwt==2.11.0 \
    --hash=sha256:35f95c1f0fbe5d5ba6e43f00271c275f7a1a4db1dab27bf708073b75318ea623 \
    --hash=sha256:94a6bde30eb5c8e04fee991062b534071fd1439ef58d2adc9ccb823e7bcd0469
+pyjwt==2.12.1 \
    --hash=sha256:28ca37c070cad8ba8cd9790cd940535d40274d22f80ab87f3ac6a713e6e8454c \
    --hash=sha256:c74a7a2adf861c04d002db713dd85f84beb242228e671280bf709d765b03672b
```

# Formatting

```
uv run bin/format.sh
```

# Copyright and licencing information
To look for files missing copyright and licencing information:

```
uv run reuse lint
```

# Neovim

You can use Neovim with the [Pyright](https://github.com/microsoft/pyright) Language Server Protococol (LSP) server. To make sure that Neovim uses the right Pyright from
this repository, run neovim inside `uv`:

```bash
uv run nvim
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
uv run ./manage.py makemessages --ignore=bin/ -l en --ignore='gunicorn.conf.py' --ignore=manage.py
```

# Develop with PostgreSQL

Projectify also works with PostgreSQL for either deployment or local
development.
Projectify supports [PostgreSQL](https://www.postgresql.org/) version 15.5 or greater.

Here's how to install PostgreSQL:

- On **macOS** (using Homebrew): `brew install postgresql` [^brew-postgres]
- On **Debian**: `sudo apt install postgresql libpq-dev`
- On **other systems**: See the [PostgresSQL documentation](https://www.postgresql.org/download/)

[^brew-postgres]: [postgresql on *brew.sh*](https://formulae.brew.sh/formula/postgresql@18#default)


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

To connect to PostgreSQL from Projectify, you need to install additional
dependencies with `uv sync`:

```bash
# This installs the dependencies from above, as well as everything needed
# for PostgreSQL
uv sync --all-groups --extra postgresql
```

Then, create a database using the `createdb` PostgreSQL command:

```bash
createdb projectify
```

Make sure that you've configured the `DATABASE_URL` string in the `.env`
file to point at your PostgreSQL `projectify` database.
These are the values for `DATABASE_URL` when connecting to PostgreSQL:

- Connect to UNIX domain socket on **Debian**:
  `DATABASE_URL = postgres://%2Fvar%2Flib%2Fpostgresql/projectify`
- Connect to UNIX domain socket on **macOS**:
  `DATABASE_URL = postgres://%2Ftmp/projectify`

# License

Projectify is licensed under the GNU Affero General Public
License Version 3 or later. Some third party dependencies are vendored in and
available under their respective licenses. Please review the license files
contained in the `LICENSES` directory located in the Projectify repository.

See `AUTHORS.txt` file for the list of contributors.

Projectify is a registered trademark by [JWP Consulting
GK](https://www.jwpconsulting.net).
