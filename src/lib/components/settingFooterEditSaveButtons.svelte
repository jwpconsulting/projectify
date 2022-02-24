<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import { _ } from "svelte-i18n";

    export let isEditMode = false;
    export let isSaving = false;

    const dispatch = createEventDispatcher();
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
            on:click={() => {
                isEditMode = false;
                dispatch("cancel");
            }}
        >
            {$_("Cancel")}
        </button>
        <button
            class:loading={isSaving}
            class="btn btn-primary btn-wide rounded-full"
            on:click={() => dispatch("save")}
        >
            Save
        </button>
    {/if}
</footer>
