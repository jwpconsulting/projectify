<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
</script>

<!-- TODO simplify and add some kind of call back -->
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("all roles not implemented"),
    }}
    label={$_("permissions-overlay.all-roles")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("owner not implemented"),
    }}
    label={$_("permissions-overlay.owner")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("maintainer not implemented"),
    }}
    label={$_("permissions-overlay.maintainer")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("member not implemented"),
    }}
    label={$_("permissions-overlay.member")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("observer not implemented"),
    }}
    label={$_("permissions-overlay.observer")}
    state="normal"
    icon={null}
/>
