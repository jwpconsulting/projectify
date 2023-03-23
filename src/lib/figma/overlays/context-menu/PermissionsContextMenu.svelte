<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
</script>

<!-- TODO simplify and add some kind of call back -->
<ContextMenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("all roles not implemented")}
    label={$_("permissions-overlay.all-roles")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.owner")}
    on:click={() => console.error("owner not implemented")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.maintainer")}
    on:click={() => console.error("maintainer not implemented")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.member")}
    on:click={() => console.error("member not implemented")}
    state="normal"
    icon={null}
/>
<ContextMenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.observer")}
    on:click={() => console.error("observer not implemented")}
    state="normal"
    icon={null}
/>
