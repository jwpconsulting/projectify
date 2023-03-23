# Projectify Frontend

## Quickstart

```
cp .env.template .env
# Edit .env
```

## Running tests & linter

```
npm run check
npm run format
```

## Identifying slowly linted files

```
npm run format | sort --key=2 -h
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
