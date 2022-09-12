<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/MenuButton.svelte";
</script>

<!-- TODO simplify and add some kind of call back -->
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("all roles not implemented")}
    label={$_("permissions-overlay.all-roles")}
    state="normal"
    icon={null}
/>
<MenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.owner")}
    on:click={() => console.error("owner not implemented")}
    state="normal"
    icon={null}
/>
<MenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.maintainer")}
    on:click={() => console.error("maintainer not implemented")}
    state="normal"
    icon={null}
/>
<MenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.member")}
    on:click={() => console.error("member not implemented")}
    state="normal"
    icon={null}
/>
<MenuButton
    kind={{ kind: "button" }}
    label={$_("permissions-overlay.observer")}
    on:click={() => console.error("observer not implemented")}
    state="normal"
    icon={null}
/>
