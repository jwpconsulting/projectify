<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Logout, User } from "@steeze-ui/heroicons";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getProfileUrl } from "$lib/urls";
</script>

<ContextMenuButton
    kind={{ kind: "a", href: getProfileUrl() }}
    label={$_("profile-overlay.my-profile")}
    state="normal"
    icon={User}
/>
<ContextMenuButton
    kind={{ kind: "a", href: "/logout" }}
    label={$_("profile-overlay.log-out")}
    state="normal"
    icon={Logout}
/>
