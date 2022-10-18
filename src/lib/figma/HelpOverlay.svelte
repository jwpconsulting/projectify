<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/buttons/MenuButton.svelte";
</script>

<MenuButton
    kind={{ kind: "a", href: "/help/basics" }}
    label={$_("help-overlay.help-and-tips")}
    state="normal"
    icon={null}
/>
<MenuButton
    kind={{ kind: "a", href: "/blog" }}
    label={$_("help-overlay.blog")}
    state="normal"
    icon={null}
/>
