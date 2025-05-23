<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Projectify Frontend

## Requirements

- Node >= v20.14.0

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

Build the frontend as using the static adapter:

```
nix build .#projectify-frontend-static
```

Run the frontend using `adapter-static` locally:

```
SVELTE_KIT_PORT=3001 nix run .#projectify-frontend-node
```

You can use the following environment variables

- `SVELTE_KIT_HOST`: The interface to bind to
- `SVELTE_KIT_PORT`: The port to listen on
- `SVELTE_KIT_PATH`: Use a unix domain socket, instead of listening on
  `SVELTE_KIT_HOST:SVELTE_KIT_PORT`

## Build Projectify frontend as Podman container

```bash
podman build \
  --target projectify-frontend \
  --tag projectify-frontend:latest \
  --file projectify-frontend.Dockerfile .
```

Run using

```bash
podman run localhost/projectify-frontend:latest
```

## Creating a new component

Note: Tools have been moved to the tools folder accessible from the monorepo
root. Look for `tools/bin/new_component`

This will create a component and story file for you automatically.

```
# Might have to run this from a poetry shell launched from within `tools/`
../tools/bin/new_component path/within/src NameOfComponent
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
src/lib/figma/overlays/context-menu/ProjectOverlay.svelte,src/lib/figma/overlays/context-menu/ProjectContextMenu.svelte
src/lib/figma/overlays/context-menu/SectionOverlay.svelte,src/lib/figma/overlays/context-menu/SectionContextMenu.svelte
src/lib/figma/overlays/context-menu/WorkspaceOverlay.svelte,src/lib/figma/overlays/context-menu/WorkspaceContextMenu.svelte
```

Then run

```
# Might have to run this from a poetry shell launched from within `tools/`
../tools/bin/rename_component.py multiple rename.csv
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
