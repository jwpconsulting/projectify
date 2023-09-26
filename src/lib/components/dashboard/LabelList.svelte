<script lang="ts">
    import LabelPill from "$lib/components/dashboard/LabelPill.svelte";
    import type { Label } from "$lib/types/workspace";

    export let labels: Label[];
</script>

{#each labels as label}
    <button>
        <LabelPill {label} />
    </button>
{/each}
