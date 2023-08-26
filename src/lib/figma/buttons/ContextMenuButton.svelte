<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";

    import type {
        ButtonAction,
        MenuButtonColor,
        MenuButtonState,
    } from "$lib/figma/types";
    import { closeContextMenu } from "$lib/stores/globalUi";

    export let label: string;
    export let icon: IconSource | null;
    export let state: MenuButtonState;
    export let color: MenuButtonColor = "base";
    export let kind: ButtonAction;

    $: colorStyle = {
        base: "text-base-content",
        primary: "text-primary",
        destructive: "text-destructive",
    }[color];
    $: style = {
        normal: "hover:bg-secondary-hover active:bg-disabled",
        accordion: "bg-background text-base-content",
    }[state];

    function action() {
        if (kind.kind !== "button") {
            throw new Error("Expected kind.action");
        }
        closeContextMenu();
        kind.action();
    }

    $: outerClass = `flex-start flex flex-row items-center gap-2 px-4 py-3 text-left text-xs font-bold focus:bg-border-focus focus:text-base-content focus:outline-none ${colorStyle} ${style}`;
</script>

{#if kind.kind === "a"}
    <a
        href={kind.href}
        class={outerClass}
        on:click={closeContextMenu}
        on:keydown={closeContextMenu}
    >
        {#if icon}
            <Icon src={icon} theme="outline" class="h-4 w-4" />
        {/if}
        <div class="first-letter:uppercase">
            {label}
        </div>
    </a>
{:else}
    <button on:click={action} on:keydown={action} class={outerClass}>
        {#if icon}
            <Icon src={icon} theme="outline" class="h-4 w-4" />
        {/if}
        <div class="first-letter:uppercase">
            {label}
        </div>
    </button>
{/if}
