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
</script>

<svelte:element
    this={kind.kind}
    href={kind.kind === "a" ? kind.href : undefined}
    on:click={kind.kind == "button" ? action : closeContextMenu}
    on:keydown={kind.kind == "button" ? action : closeContextMenu}
    class={`flex-start flex flex-row items-center gap-2 px-4 py-3 text-left text-xs font-bold focus:bg-border-focus focus:text-base-content focus:outline-none ${colorStyle} ${style}`}
>
    {#if icon}
        <Icon src={icon} theme="outline" class="h-4 w-4" />
    {/if}
    <div class="first-letter:uppercase">
        {label}
    </div>
</svelte:element>
