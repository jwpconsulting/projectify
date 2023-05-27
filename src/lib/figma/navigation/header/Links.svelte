<script lang="ts">
    import { _ } from "svelte-i18n";
    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
</script>

<HeaderButton
    type={{ kind: "button" }}
    label={$_("header.features")}
    action={{ kind: "a", href: "/features" }}
/>
<HeaderButton
    type={{ kind: "button" }}
    label={$_("header.solutions")}
    action={{ kind: "a", href: "/solutions" }}
/>
<!-- what is this?
<HeaderButton
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.resources")}
    action={{ kind: "a", href: "/resources" }}
/>
-->
<!-- what is this?
<HeaderButton
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.company")}
    action={{ kind: "a", href: "/company" }}
/>
-->
<HeaderButton
    type={{ kind: "button" }}
    label={$_("header.pricing")}
    action={{ kind: "a", href: "/pricing" }}
/>
