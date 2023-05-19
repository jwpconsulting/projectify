# Page load function

Use svelte kit types that are generated automatically for great comfort. This
goes in `+page.ts`. `myParam` is part of the route like `/[myParam]/...`

```
import type { PageLoadEvent } from "./$types";

interface Data {
    theThing: TheThing
}

export async function load({
    params: { myParam },
    fetch,
}: PageLoadEvent): Promise<Data> {
    // If thing is fetched, use the fetch argument above
    const theThing = new TheThing();
    return { theThing };
}

export const prerender = false;
export const ssr = false;
```

Then, when you use the data inside the svelte page, you can access them like
so:

```
<script lang="ts">
    import type { PageData } from "./$types";

    export let data: PageData;

    const { theThing } = data;
</script>

I have loaded { theThing }!
```

## Redirecting

Import the following inside `+page.ts`:

```
import { redirect } from "@sveltejs/kit";
```

And throw the following inside the load function:

```
const theUrl = "/";
throw redirect(302, theUrl)
```

Some of the redirect codes you might consider can be found in the [mdn web
docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections). 302
isn't too bad.

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
import { openContextMenu } from "$lib/stores/globalUi";
openContextMenu(contextMenuType, contextMenuOpensHere)
```

# Creating an InputField

Say you want an `<input>` field called "name", then create the following:

```
<script lang="ts">
    import { _ } from "svelte-i18n";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
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

- `anchorTop`, and
- `anchorBottom`

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

# Button

Let's create a medium-sized, blue primary Button with the label "Click me".

```
<script lang="ts">
    import Button from "$lib/figma/buttons/Button.svelte";
</script>

<Button
    style={{ kind: "primary" }}
    size="medium"
    color="blue"
    label="Click me"
    disabled={false}
/>
```
