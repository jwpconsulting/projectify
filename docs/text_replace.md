<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Text replacement

Some general ideas on how to do text replacement over many files.

It's assumed that the following programs are available in the terminal:

- NVIM v0.9.4
- ag version 2.2.0
- fd 8.7.1

# Finding instances using a regular expression

We want to replace all mentions of "workspace board" with "project".

Workspace board can appear in many variants, here are hopefully all of them:

- `WorkspaceBoard`
- `WorkspaceBoards`
- `workspaceBoard`
- `workspaceBoards`
- `workspace_board`
- `workspace_boards`
- `workspace-board`
- `workspace-boards`
- `workspace board`
- `workspace boards`
- `Workspace board`
- `Workspace boards`

There is a certain order of priority for search results, if we want to not have
partial replacements, like when searching for `workspace board`, and then the
result `[workspace board]s` being replaced with `projects`, which I suppose is
correct, since `projects` happens to be correct, but not every replacement can
rely on English plural 's' being at the right place.

Furthermore, we'd like to avoid replacing Django DB migrations, since they rely
on not being changed at all, and serving as a historical record of the state of
models serves as a reference on how to perform migration changes.

We can list all lines containing the above string instances with ag:

```fish
ag "([wW]orkspace[_\- ]?[bB]oard)s?" .
```

Similarly, we can find all instances of _workspace board section_, if we'd like
to rename it to just _section_:

```fish
ag "([wW]orkspace[_ -]?[bB]oard[_ -][sS]ection)s?" .
```

Similarly, all files named after _workspace board section_ would have to be
renamed, but this can be done manually.

We rename workspace board sections first, so that there is no intermediate step
in which they are called project sections and then have to be renamed again
anyway.

# Interactive replace

It's better to interactively replace strings, to have some more control and
feedback over the result. We pass the `--files-with-matches` flag to ag to get
just the filenames. Then we can use nvim to go over each file and edit it like
so:

```fish
nvim (ag \
  --files-with-matches \
  "([wW]orkspace[_ -]?[bB]oard[_ -][sS]ection)s?" \
  . \
)
```

Inside nvim, we can run:

```vim
bufdo %s/\v([wW]orkspace[_ -]?[bB]oard[_ -]([sS]ection))(s?)/\2\3/gce
```

To combine it, we have

```fish
nvim (ag \
  --files-with-matches \
  "([wW]orkspace[_ -]?[bB]oard[_ -][sS]ection)s?" \
  . \
) -c "bufdo %s/\v([wW]orkspace[_ -]?[bB]oard[_ -]([sS]ection))(s?)/\2\3/gce"
```

An edge case to consider is replacing `Workspace board sections` appropriately
with `Sections`, not `sections`. We therefore decide to split the renaming in
two different steps, and also simplify the parentheses:

```fish
nvim (ag \
  --files-with-matches \
  "([wW]orkspace[_ -]?[bB]oard[_ -][sS]ection)s?" \
  . \
) -c "bufdo %s/\vworkspace[_ -]?[bB]oard[_ -][sS]ection(s?)/section\1/gce"
```

One more tweak, since the author's nvim has `gdefault` enabled, _by default_,
the `/gce` flag _deactivates_ the global replace flag
([see nvim docs](https://neovim.io/doc/user/options.html#'gdefault')), so we
remove the `g` flag. Some more fixes:

- We tell `ag` to ignore paths with the name `migrations` as well, and
- to ignore this very markdown file that we are editing.
- We add a forgotten `?` character after the second character class that
  separates "board" and "section" to make a character between the two words
  optional.

```fish
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "([wW]orkspace[_ -]?[bB]oard[_ -]?[sS]ection)s?" \
  . \
) -c "bufdo %s/\vworkspace[_ -]?[bB]oard[_ -]?[sS]ection(s?)/section\1/ce"
```

We save with `:wall` and quit.

Now, to replace the uppercase 'W' instances of workspace board section names,
we run the following:

```fish
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "(Workspace[_ -]?[bB]oard[_ -]?[sS]ection)s?" \
  . \
) -c "bufdo %s/\vWorkspace[_ -]?[bB]oard[_ -]?[sS]ection(s?)/Section\1/ce"
```

The next thing to do is rename all file names, starting with folders. We use
fdfind here, and pass the `--exec` flag to rename each result. Like ag, fdfind
respects `.gitignore` files, wheres grep/find do not. That makes our lives as
developers easier. We can list all folders containing a workspace board section
name like so:

```fish
fd --type directory \
  "workspace[_ -]?[bB]oard[_ -]?[sS]ections?" \
  .
# (there are no results for Workspace with uppercase w)
```

There are four folders, and we can rename them like so:

```fish
for f in (
  fd --type directory \
    "workspace[_ -]?[bB]oard[_ -]?[sS]ections?" \
    .
)
  echo "Moving $f"
  set -l dir (dirname $f)
  read -l -P "New path: $dir/" base || break
  echo "Moving to $base"
  git mv -v $f $dir/$base || break
end
```

To rename the files, we run

```fish
for f in (
  fd --type file \
    "workspace[_ -]?[bB]oard[_ -]?[sS]ections?" \
    --exclude migrations \
    .
)
  echo "Moving $f"
  set -l dir (dirname $f)
  read -l -P "New path: $dir/" base || break
  echo "Moving to $dir/$base"
  git mv -v $f $dir/$base || break
end
```

# Now the same for workspace boards

Since it we couldn't rename all instance of workspace_board_section in the
backend, we have to be careful.

For lower case:

```fish
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "workspace[_ -]?[bB]oard[_ -]?s?" \
  . \
) -c "bufdo %s/\vworkspace[_ -]?[bB]oard(s?)([_ -][sS]ection)@!/project\1/ce"
```

For upper case:

```fish
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "Workspace[_ -]?[bB]oard[_ -]?s?" \
  . \
) -c "bufdo %s/\vWorkspace[_ -]?[bB]oard(s?)(_ -][sS]ection)@!/Project\1/ce"
```

For folders:

```fish
for f in (
  fd --type directory \
    "[wW]orkspace[_ -]?[bB]oard[_ -]?s?" \
    .
)
  echo "Moving $f"
  set -l dir (dirname $f)
  read -l -P "New path: $dir/" base || break
  echo "Moving to $base"
  git mv -v $f $dir/$base || break
end
```

The above might have to be run multiple times.

For files:

```
for f in (
  fd --type file \
    "[wW]orkspace[_ -]?[bB]oard[_ -]?s?" \
    --exclude migrations \
    .
)
  echo "Moving $f"
  set -l dir (dirname $f)
  read -l -P "New path: $dir/" base || break
  echo "Moving to $dir/$base"
  git mv -v $f $dir/$base || break
end
```

# Renaming member to contributor

In order to rename workspace users to members, we want to first change the role
member to be contributor, to remove ambiguity.

```fish
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "MEMBER" \
  . \
) -c "bufdo %s/\vMEMBER/CONTRIBUTOR\1/ce"
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "Member" \
  . \
) -c "bufdo %s/\vMember/Contributor\1/ce"
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "member" \
  . \
) -c "bufdo %s/\vmember/contributor\1/ce"
```

# Renaming workspace user to team member

Rename strings, making the vim regex case sensitive:

```fish
nvim (ag \
  --files-with-matches \
  --ignore migrations \
  --ignore docs/text_replace.md \
  "workspace[_ -]?users?" \
  . \
) -c "bufdo %s/\C\vworkspace([_ -]?)user(s?)/team\1member\2/ce" \
  -c "bufdo %s/\C\vWorkspace([_ -]?)user(s?)/Team\1member\2/ce" \
  -c "bufdo %s/\C\vworkspace([_ -]?)User(s?)/team\1Member\2/ce" \
  -c "bufdo %s/\C\vWorkspace([_ -]?)User(s?)/Team\1Member\2/ce"
```

Rename files

```fish
for f in (
  fd \
    "[wW]orkspace[_ -]?[uU]ser[_ -]?s?" \
    --exclude migrations \
    .
)
  echo "Moving $f"
  set -l dir (dirname $f)
  read -l -P "New path: $dir/" base || break
  echo "Moving to $dir/$base"
  git mv -v $f $dir/$base || break
end
```

# Replacing licenses with short identifiers

Three scripts:

```sed
# replace_header_ts.sed
/^\/\*$/!{
    p;
    b
}
n
/Copyright \(C\) .+$/{
    :a
    s/^ \*  Copyright \(C\) (.+)$/\/\/ SPDX-FileCopyrightText: \1/p
    n
    /^ \*\/$/b
    ba
}
p
```

```sed
# replace_header_svelte.sed
/<!--$/!{
    p;
    b
}
/<!--$/{
    n
    /    Copyright \(C\) .*/{
        :a
        s/^    Copyright \(C\) (.+)$/<!-- SPDX-FileCopyrightText: \1 -->/p
        n
        \%    along with this program.  If not, see <https://www.gnu.org/licenses/>\.%!ba
        n
        /\\n-->/b
    }
}
```

```sed
# replace_header_py.sed
/\# Copyright \(C\) .+$/!{
    p;
    b
}
/\# Copyright \(C\) .+$/{
    s/\# Copyright \(C\) (.+)$/# SPDX-FileCopyrightText: \1/p
    :a
    n
    \%# along with this program.  If not, see <https://www.gnu.org/licenses/>.%!ba
    d
}
p
```

Example usage:

```bash
sed -i -n -E -f replace_header_svelte.sed frontend/**.svelte
sed -i -n -E -f replace_header_py.sed backend/**.py
sed -i -n -E -f replace_header_ts.sed frontend/**.ts
```
