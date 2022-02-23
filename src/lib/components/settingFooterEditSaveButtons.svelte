<script lang="ts">
    import { _ } from "svelte-i18n";

    export let isEditMode = false;
</script>

<footer class="flex item-center justify-center space-x-2">
    {#if !isEditMode}
        <button
            class="btn btn-primary btn-outline btn-wide rounded-full"
            on:click={() => (isEditMode = true)}
        >
            {$_("Edit")}
        </button>
    {:else}
        <button
            class="btn btn-primary btn-outline btn-wide rounded-full"
            on:click={() => (isEditMode = false)}
        >
            {$_("Cancel")}
        </button>
        <button class="btn btn-primary btn-wide rounded-full"> Save </button>
    {/if}
</footer>
