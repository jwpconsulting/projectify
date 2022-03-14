<script lang="ts">
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import { getColorFromInx } from "$lib/utils/colors";
    function selectLabel(label) {
        console.log(label);
    }
</script>

{#each $currentWorkspaceLabels as label}
    <a
        style="{`--color:${getColorFromInx(label.color).style};`};"
        href="/"
        class="label whitespace-nowrap font-bold text-xs px-3 py-1 m-1 rounded-full border"
        on:click|preventDefault={() => selectLabel(label)}
    >
        {label.name}
    </a>
{/each}

<style lang="scss">
    .label {
        --opacity: 1;
        --bg-opacity: 0.3;
        color: rgba(var(--color) / var(--opacity));
        background-color: rgba(var(--color) / var(--bg-opacity));
    }
</style>
