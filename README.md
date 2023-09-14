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
PIPENV_PIPFILE=Pipfile-tools pipenv sync --dev
```

And then

```
PIPENV_PIPFILE=Pipfile-tools pipenv run bin/rename_component.py
```

How to test

```
PIPENV_PIPFILE=Pipfile-tools pipenv run flake8
PIPENV_PIPFILE=Pipfile-tools pipenv run mypy
```

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
PIPENV_PIPFILE=Pipfile-tools pipenv run bin/rename_component.py multiple rename.csv
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
