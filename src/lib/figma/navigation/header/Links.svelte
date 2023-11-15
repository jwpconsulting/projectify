<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
</script>

<HeaderButton
    type={{ kind: "button" }}
    label={$_("navigation.header.features")}
    action={{ kind: "a", href: "/features" }}
/>
<HeaderButton
    type={{ kind: "button" }}
    label={$_("navigation.header.solutions")}
    action={{ kind: "a", href: "/solutions" }}
/>
<!-- what is this?
<HeaderButton
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("navigation.header.company")}
    action={{ kind: "a", href: "/company" }}
/>
-->
<HeaderButton
    type={{ kind: "button" }}
    label={$_("navigation.header.pricing")}
    action={{ kind: "a", href: "/pricing" }}
/>
<HeaderButton
    type={{ kind: "button" }}
    label={$_("navigation.header.help")}
    action={{ kind: "a", href: "/help" }}
/>
