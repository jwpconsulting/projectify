# Opening context menu

Decide which kind of context menu you need

```
// See src/lib/types/ui.ts ContextMenuType
const contextMenuType = {
    kind: "theKind",
    ...additionalData
}
```

You have to bind show this somewhere, so bind an anchor HTMLElement:

```
<div bind:this={contextMenuOpensHere} />
```

Open it up by calling

```
import { openContextMenu } from "$lib/stores/global-ui";
openContextMenu(contextMenuType, contextMenuOpensHere)
```

# Creating an InputField

Say you want an `<input>` field called "name", then create the following:

```
<script lang="ts">
    import { _ } from "svelte-i18n";
    import InputField from "$lib/figma/input-fields";
</script>

<InputField
    style={{kind: "field", inputType: "text"}}
    placeholder={$_("translate-me")}
    name="name"
    label={$_("translate-me")}
/>
```

Some variations can be as follows.

## Password entry

```
<InputField
    style={{kind: "field", inputType: "password"}}
    placeholder={$_("translate-me")}
    name="password"
    label={$_("translate-me")}
/>
```

## Search

```
<InputField
    style={{kind: "search"}}
    placeholder={$_("translate-me")}
    name="searchInput"
    label={$_("translate-me")}
/>
```

## Anchors

You can add an anchor top right or bottom right using the following two props:

-   `anchorTop`, and
-   `anchorBottom`

These should be an object like the following:

```js
{
    href: "https://example.com",
    label: "Example Label",
}
```

This can be pieced together like so:

```
<InputField
    style={{kind: "search"}}
    placeholder={$_("translate-me")}
    name="searchInput"
    label={$_("translate-me")}
    anchorTop={{href:"#help", label: "About the task search"}}
/>
```
