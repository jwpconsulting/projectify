<script lang="ts">
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
</script>

<Layout>
    <!-- TODO simplify and add some kind of call back -->
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("all roles not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.all-roles")}
        state="normal"
        icon={null}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("owner not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.owner")}
        state="normal"
        icon={null}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("maintainer not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.maintainer")}
        state="normal"
        icon={null}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("member not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.member")}
        state="normal"
        icon={null}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("observer not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.observer")}
        state="normal"
        icon={null}
    />
</Layout>
