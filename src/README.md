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
