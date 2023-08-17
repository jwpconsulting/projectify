<script lang="ts">
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
</script>

<ContextMenuButton
    kind={{ kind: "a", href: "/help/basics" }}
    label={$_("help-overlay.help-and-tips")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{ kind: "a", href: "/blog" }}
    label={$_("help-overlay.blog")}
    state="normal"
    icon={null}
/>
