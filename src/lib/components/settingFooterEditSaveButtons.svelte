<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import { _ } from "svelte-i18n";

    export let isEditMode = false;
    export let isSaving = false;

    const dispatch = createEventDispatcher();
</script>

<footer
    class="flex item-center justify-center space-x-2 py-1 border-t border-base-300 pt-4 mt-4"
>
    {#if !isEditMode}
        <slot />
        <button
            class="btn btn-primary btn-outline grow max-w-[200px] rounded-full"
            on:click={() => (isEditMode = true)}
        >
            {$_("Edit")}
        </button>
    {:else}
        <button
            class="btn btn-primary btn-outline grow max-w-[200px] rounded-full"
            on:click={() => {
                isEditMode = false;
                dispatch("cancel");
            }}
        >
            {$_("Cancel")}
        </button>
        <button
            class:loading={isSaving}
            class="btn btn-primary grow max-w-[200px] rounded-full"
            on:click={() => dispatch("save")}
        >
            {$_("Save")}
        </button>
    {/if}
</footer>
