# Projectify Frontend

## Quickstart

```
cp .env.template .env
# Edit .env
```

## Running tests & linter

```
npm run fix
npm run check
```

## Identifying slowly linted files

```
npm run fix | sort --key=2 -h
```

## Installing the python tools

```
poetry install --all-extras
```

And then

```
poetry run bin/rename_component.py
```

How to test

```
poetry run flake8
poetry run mypy
```

## Using Nix Flake and direnv

You can automatically make Node and other tools available using the nix flake
provided in this repository. To get started, you need to have the following
installed and configured on your system:

- [Nix](https://nixos.org/download#download-nix)
- [Nix flakes](https://nixos.wiki/wiki/Flakes)
- [Direnv](https://direnv.net/)
- [nix-direnv](https://github.com/nix-community/nix-direnv)

If everything is configured correctly, running `direnv allow` from the
root directory of this repository will make all tools available. Setting up
nix was a complicated process and took some time to get right.
If you skip NixOS, home manager, and so on, you might be able to finish it in
a few hours. If you have any questions, please contact the maintainers.

## Creating a new component

This will create a component and story file for you automatically.

```
bin/new_component path/within/src NameOfComponent
```

# Bulk renaming components

This is from a recent renaming session. First, create a file called
`rename.csv` and put in the following:

```
src_cmp,dst_cmp
src/lib/figma/overlays/context-menu/HelpOverlay.svelte,src/lib/figma/overlays/context-menu/HelpContextMenu.svelte
src/lib/figma/overlays/context-menu/PermissionsOverlay.svelte,src/lib/figma/overlays/context-menu/PermissionsContextMenu.svelte
src/lib/figma/overlays/context-menu/ProfileOverlay.svelte,src/lib/figma/overlays/context-menu/ProfileContextMenu.svelte
src/lib/figma/overlays/context-menu/SideNavOverlay.svelte,src/lib/figma/overlays/context-menu/SideNavContextMenu.svelte
src/lib/figma/overlays/context-menu/TaskOverlay.svelte,src/lib/figma/overlays/context-menu/TaskContextMenu.svelte
src/lib/figma/overlays/context-menu/WorkspaceBoardOverlay.svelte,src/lib/figma/overlays/context-menu/WorkspaceBoardContextMenu.svelte
src/lib/figma/overlays/context-menu/WorkspaceBoardSectionOverlay.svelte,src/lib/figma/overlays/context-menu/WorkspaceBoardSectionContextMenu.svelte
src/lib/figma/overlays/context-menu/WorkspaceOverlay.svelte,src/lib/figma/overlays/context-menu/WorkspaceContextMenu.svelte
```

Then run

```
poetry run bin/rename_component.py multiple rename.csv
```

# Updating Storybook

Let's say a new version of Storybook is out. Instead of using `npm update` on
all the storybook packages, use

```
npx sb@latest upgrade
```

It might fail around the end, with a

```
🔎 checking possible migrations..
[Storybook automigrate] ❌ Unable to determine storybook version so the automigrations will be skipped.
  🤔 Are you running automigrate from your project directory? Please specify your Storybook config directory with the --config-dir flag.
  ERR! TypeError: Cannot convert undefined or null to object
  ERR!     at Function.values (<anonymous>)
  ERR!     at automigrate (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/cli/dist/generate.js:321:743)
  ERR!     at async doUpgrade (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/cli/dist/generate.js:394:2893)
  ERR!     at async withTelemetry (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/core-server/dist/index.js:35:3422)
  ERR!     at async upgrade (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/cli/dist/generate.js:394:3336)
  ERR!  TypeError: Cannot convert undefined or null to object
  ERR!     at Function.values (<anonymous>)
  ERR!     at automigrate (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/cli/dist/generate.js:321:743)
  ERR!     at async doUpgrade (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/cli/dist/generate.js:394:2893)
  ERR!     at async withTelemetry (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/core-server/dist/index.js:35:3422)
  ERR!     at async upgrade (/home/godtiercheesemelt/.npm/_npx/7870b4b551bffaf6/node_modules/@storybook/cli/dist/generate.js:394:3336)
```

Someone [else](https://github.com/vercel/turbo/issues/4612) appears to have
this issue as well.

# Running LSP

For vim, you might enhance your config with something like this:

```lua
lspconfig.tsserver.setup {
    cmd = { 'npm', 'run', 'typescript-language-server', '--', '--stdio' },
}
lspconfig.svelte.setup {
    cmd = { 'npm', 'run', 'svelteserver', '--', '--stdio' },
}
```

Also refer to these resources:

- [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig/tree/master)

## License

Copyright (C) 2021-2024 JWP Consulting GK

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
