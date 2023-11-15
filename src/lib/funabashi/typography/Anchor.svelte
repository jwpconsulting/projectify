<script lang="ts">
    import type { AnchorSize } from "$lib/funabashi/types";

    export let href: string;
    export let label: string;
    export let size: AnchorSize = "normal";

    let anchorClass: string;
    $: anchorClass = {
        // TODO remove this class
        extraSmall: "text-xs",
        // TODO remove this class
        small: "text-sm",
        normal: "text-base",
        large: "text-lg",
    }[size];
</script>

<a
    {href}
    class={`text-primary hover:text-primary-hover active:text-primary-pressed ${anchorClass}`}
    >{label}</a
>
