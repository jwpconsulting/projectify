<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

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

Some of the redirect codes you might consider can be found in the
[mdn web docs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections).
302 isn't too bad.

# Opening context menu

Decide which kind of context menu you need

```
import type { ContextMenuType } from "$lib/types/ui";
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

# Opening constructive overlay

Decide the type

```
import type { ConstructiveOverlayType } from "$lib/types/ui";
const constructiveOverlayType = {
    kind: "theKind",
    ...additionalDate,
};
```

The action to be performed might be removed (no overlay uses it):

```
const action = {
    kind: "sync",
    action: console.log,
};
```

Then open it

```
openConstructiveOverlay(constructiveOverlayType, action);
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

# Stories

## Simulate mobile screen

In a stories.ts file, add the following:

```
import { mobileParameters } from "$lib/storybook";

export const Mobile: Story = {
    parameters: mobileParameters,
};
```

## Using typed stories

Convert this

```typescript
export default {
  component: Component,
};
```

into

```typescript
import type { Meta, StoryObj } from "@storybook/svelte";
const meta: Meta<ComponentName> = {
  component: ComponentName,
  argTypes: {},
  args: {},
};
export default meta;
```

Then, for each story:

```typescript
export const StoryName = () => ({
  Component: ComponentName,
});
```

becomes

```typescript
type Story = StoryObj<ComponentName>;

export const StoryName: Story = {
  args: {},
};
```
