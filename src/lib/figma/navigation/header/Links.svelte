<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/funabashi/buttons/Button.svelte";
</script>

<Button
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.features")}
    action={{ kind: "a", href: "/features" }}
/>
<Button
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.solutions")}
    action={{ kind: "a", href: "/solutions" }}
/>
<!-- what is this?
<Button
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.resources")}
    action={{ kind: "a", href: "/resources" }}
/>
-->
<!-- what is this?
<Button
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.company")}
    action={{ kind: "a", href: "/company" }}
/>
-->
<Button
    style={{ kind: "tertiary", icon: null }}
    color="blue"
    disabled={false}
    size="medium"
    label={$_("header.pricing")}
    action={{ kind: "a", href: "/pricing" }}
/>
