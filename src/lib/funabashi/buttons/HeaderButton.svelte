<script lang="ts">
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import type { ButtonAction, HeaderButtonType } from "$lib/funabashi/types";
    import { filterKey } from "$lib/stores/globalUi";

    export let label: string;
    export let type: HeaderButtonType;
    export let action: ButtonAction;

    const dropdownClass =
        "active:text-primary flex max-w-fit flex-row items-center gap-2 rounded-lg p-2 text-base-content hover:text-primary focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2";
    const buttonClass =
        "text-base-content flex max-w-fit flex-row items-center gap-2 rounded-lg p-2 hover:text-primary focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:text-primary";

    $: dropdownButtonSrc =
        type.kind === "dropdown" && type.open ? ChevronUp : ChevronDown;
</script>

{#if action.kind === "button"}
    {#if type.kind === "dropdown"}
        <button
            on:click={action.action}
            on:keydown={action.action}
            class={dropdownClass}
        >
            <div class="text-base font-bold capitalize">
                {label}
            </div>
            <Icon src={dropdownButtonSrc} theme="outline" class="h-4 w-4" />
        </button>
    {:else}
        <button
            on:click={action.action}
            on:keydown={action.action}
            class={buttonClass}
        >
            <div class="text-base font-bold">
                {label}
            </div>
        </button>
    {/if}
{:else if action.kind === "a"}
    <!-- we just ignore the dropdown case for now -->
    <a
        href={action.href}
        class={buttonClass}
        on:click={action.onInteract}
        on:keydown={action.onInteract && filterKey("Enter", action.onInteract)}
    >
        <div class="text-base font-bold">
            {label}
        </div>
    </a>
{/if}
