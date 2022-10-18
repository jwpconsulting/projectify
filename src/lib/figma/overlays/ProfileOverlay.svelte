<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/buttons/MenuButton.svelte";
    import { getProfileUrl } from "$lib/urls";
    import { User, Logout } from "@steeze-ui/heroicons";
</script>

<MenuButton
    kind={{ kind: "a", href: getProfileUrl() }}
    label={$_("profile-overlay.my-profile")}
    state="normal"
    icon={User}
/>
<MenuButton
    kind={{ kind: "button" }}
    on:click={() => console.error("not implemented")}
    label={$_("profile-overlay.log-out")}
    state="normal"
    icon={Logout}
/>
