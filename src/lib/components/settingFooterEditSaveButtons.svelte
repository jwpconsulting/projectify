<script lang="ts">
    import { _ } from "svelte-i18n";

    export let save: () => void;
    export let cancel: () => void;
    export let state: "viewing" | "editing" | "saving";
</script>

<footer
    class="item-center mt-4 flex justify-center space-x-2 border-t border-base-300 py-1 pt-4"
>
    {#if state === "viewing"}
        <slot />
        <button
            class="btn btn-outline btn-primary max-w-[200px] grow rounded-full"
            on:click={() => (state = "editing")}
        >
            {$_("Edit")}
        </button>
    {:else}
        <button
            class="btn btn-outline btn-primary max-w-[200px] grow rounded-full"
            on:click={() => {
                state = "viewing";
                cancel();
            }}
        >
            {$_("Cancel")}
        </button>
        <button
            class:loading={state === "saving"}
            class="btn btn-primary max-w-[200px] grow rounded-full"
            on:click={save}
        >
            {$_("Save")}
        </button>
    {/if}
</footer>
