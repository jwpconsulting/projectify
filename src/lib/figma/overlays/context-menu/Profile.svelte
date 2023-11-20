<script lang="ts">
    import { Logout, User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { getProfileUrl } from "$lib/urls";
    import { logOutUrl } from "$lib/urls/user";
</script>

<Layout>
    <ContextMenuButton
        kind={{ kind: "a", href: getProfileUrl() }}
        label={$_("overlay.context-menu.profile.my-profile")}
        state="normal"
        icon={User}
    />
    <ContextMenuButton
        kind={{ kind: "a", href: logOutUrl }}
        label={$_("overlay.context-menu.profile.log-out")}
        state="normal"
        icon={Logout}
    />
</Layout>
