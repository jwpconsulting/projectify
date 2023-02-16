<script lang="ts">
    import type { Label } from "$lib/types/workspace";
    import LabelC from "$lib/figma/buttons/Label.svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Tag } from "@steeze-ui/heroicons";

    export let labels: Label[];
</script>

<div class="flex flex-row items-center gap-4">
    <Icon src={Tag} class="w-6" theme="outline" />
    {#each labels as label}
        <LabelC label={{ kind: "label", label }} />
    {/each}
    <LabelC label={{ kind: "applyLabel" }} />
</div>
