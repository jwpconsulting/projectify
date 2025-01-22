---
title: Heroicons used in Projectify
date: 2025-01-21
author: Justus Perlwitz
---
<!--
SPDX-FileCopyrightText: 2025 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

This command searches for usages of heroicons in the frontend:

```bash
cd frontend/
ag 'import {[^}]+} from "@steeze-ui/heroicons"' --only-matching | sed -n -E 's/src\/.+.svelte:[0-9]+: +([A-Za-z]+),/\1/p' | sort -u
```

These are all the hero icons that we use:

```
Archive
ArrowCircleLeft
ArrowCircleRight
ArrowDown
ArrowUp
ArrowsExpand
CheckCircle
ChevronDown
ChevronUp
Cog
DotsHorizontal
DotsVertical
Duplicate
Folder
LightBulb
Pencil
Plus
Selector
SortAscending
SortDescending
SwitchVertical
Tag
Trash
User
Users
X
```

Converted to kebab case with `sed 's/[A-Z]/-\l&/g'` and edited a bit:

```
archive.svg
arrow-circle-left.svg
arrow-circle-right.svg
arrow-down.svg
arrow-up.svg
arrows-expand.svg
check-circle.svg
chevron-down.svg
chevron-up.svg
cog.svg
dots-horizontal.svg
dots-vertical.svg
duplicate.svg
folder.svg
light-bulb.svg
pencil.svg
plus.svg
selector.svg
sort-ascending.svg
sort-descending.svg
switch-vertical.svg
tag.svg
trash.svg
user.svg
users.svg
x.svg
```

Copy all:

```fish
for file in archive.svg arrow-circle-left.svg arrow-circle-right.svg arrow-down.svg arrow-up.svg arrows-expand.svg check-circle.svg chevron-down.svg chevron-up.svg cog.svg dots-horizontal.svg dots-vertical.svg duplicate.svg folder.svg light-bulb.svg pencil.svg plus.svg selector.svg sort-ascending.svg sort-descending.svg switch-vertical.svg tag.svg trash.svg user.svg users.svg x.svg
  cp ../heroicons/src/outline/$file backend/projectify/static/heroicons
end
```
