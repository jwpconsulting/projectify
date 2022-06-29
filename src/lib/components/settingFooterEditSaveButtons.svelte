<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import { _ } from "svelte-i18n";

    export let isEditMode = false;
    export let isSaving = false;

    const dispatch = createEventDispatcher();
</script>

<footer
    class="item-center mt-4 flex justify-center space-x-2 border-t border-base-300 py-1 pt-4"
>
    {#if !isEditMode}
        <slot />
        <button
            class="btn btn-outline btn-primary max-w-[200px] grow rounded-full"
            on:click={() => (isEditMode = true)}
        >
            {$_("Edit")}
        </button>
    {:else}
        <button
            class="btn btn-outline btn-primary max-w-[200px] grow rounded-full"
            on:click={() => {
                isEditMode = false;
                dispatch("cancel");
            }}
        >
            {$_("Cancel")}
        </button>
        <button
            class:loading={isSaving}
            class="btn btn-primary max-w-[200px] grow rounded-full"
            on:click={() => dispatch("save")}
        >
            {$_("Save")}
        </button>
    {/if}
</footer>
