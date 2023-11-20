<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
</script>

<HeaderButton
    label={$_("navigation.header.solutions")}
    action={{ kind: "a", href: "/solutions" }}
/>
<HeaderButton
    label={$_("navigation.header.pricing")}
    action={{ kind: "a", href: "/pricing" }}
/>
<HeaderButton
    label={$_("navigation.header.help")}
    action={{ kind: "a", href: "/help" }}
/>
