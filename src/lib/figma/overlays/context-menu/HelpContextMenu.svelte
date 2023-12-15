<script lang="ts">
    // Rename to Help.svelte (other context menu names can be simplified as
    // well)
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
</script>

<Layout>
    <ContextMenuButton
        kind={{ kind: "a", href: "/help/basics" }}
        label={$_("overlay.context-menu.help.help-and-tips")}
        state="normal"
    />
    <ContextMenuButton
        kind={{ kind: "a", href: "/blog" }}
        label={$_("overlay.context-menu.help.blog")}
        state="normal"
    />
</Layout>
