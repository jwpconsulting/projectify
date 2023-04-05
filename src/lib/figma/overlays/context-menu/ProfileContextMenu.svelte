<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getProfileUrl } from "$lib/urls";
    import { User, Logout } from "@steeze-ui/heroicons";
</script>

<ContextMenuButton
    kind={{ kind: "a", href: getProfileUrl() }}
    label={$_("profile-overlay.my-profile")}
    state="normal"
    icon={User}
/>
<ContextMenuButton
    kind={{ kind: "button", action: () => console.error("not implemented") }}
    label={$_("profile-overlay.log-out")}
    state="normal"
    icon={Logout}
/>
