<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import type { HeaderButtonType } from "$lib/funabashi/types";
    import type { ButtonAction } from "$lib/figma/types";

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

{#if type.kind == "dropdown"}
    {#if action.kind === "button"}
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
        <a href={action.href} class={dropdownClass}>
            <div class="text-base font-bold capitalize">
                {label}
            </div>
            <Icon src={dropdownButtonSrc} theme="outline" class="h-4 w-4" />
        </a>
    {/if}
{:else if action.kind === "button"}
    <button
        on:click={action.action}
        on:keydown={action.action}
        class={buttonClass}
    >
        <div class="text-base font-bold capitalize">
            {label}
        </div>
    </button>
{:else}
    <a href={action.href} class={buttonClass}>
        <div class="text-base font-bold capitalize">
            {label}
        </div>
    </a>
{/if}
