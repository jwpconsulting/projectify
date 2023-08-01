<script lang="ts">
    import type { AnchorSize } from "$lib/figma/types";

    export let href: string;
    export let label: string;
    export let size: AnchorSize;

    let anchorClass: string;
    $: anchorClass = {
        extraSmall: "text-xs",
        normal: "text-base",
        large: "text-lg",
    }[size];
</script>

<a
    {href}
    class={`text-primary hover:text-primary-hover active:text-primary-pressed ${anchorClass}`}
    >{label}</a
>
