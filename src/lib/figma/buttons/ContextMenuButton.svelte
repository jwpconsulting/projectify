<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";

    import type { MenuButtonColor, MenuButtonState } from "$lib/figma/types";
    import type { ButtonAction } from "$lib/funabashi/types";
    import { closeContextMenu } from "$lib/stores/globalUi";

    export let label: string;
    export let icon: IconSource | undefined = undefined;
    export let iconRight: IconSource | undefined = undefined;
    export let state: MenuButtonState;
    export let color: MenuButtonColor = "base";
    export let kind: ButtonAction & { kind: "button" | "a" };
    export let closeOnInteract = true;

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
            throw new Error("Expected button");
        }
        if (kind.disabled) {
            throw new Error("Button is disabled");
        }
        if (closeOnInteract) {
            closeContextMenu();
        }
        kind.action();
    }

    function interact() {
        if (kind.kind !== "a") {
            throw new Error("Expected a");
        }
        if (closeOnInteract) {
            closeContextMenu();
        }
        if (kind.onInteract) {
            kind.onInteract();
        }
    }

    $: outerClass = `w-full flex-start flex flex-row items-center gap-2 px-4 py-2 text-left text-sm font-bold ${colorStyle} ${style}`;
</script>

{#if kind.kind === "a"}
    <a href={kind.href} class={outerClass} on:click={interact}>
        {#if icon}<Icon src={icon} theme="outline" class="h-4 w-4" />{/if}
        <div>{label}</div>
        {#if iconRight}
            <Icon src={iconRight} theme="outline" class="h-4 w-4" />{/if}
    </a>
{:else}
    <button disabled={kind.disabled} on:click={action} class={outerClass}>
        {#if icon}<Icon src={icon} theme="outline" class="h-4 w-4" />{/if}
        <div>{label}</div>
        {#if iconRight}
            <Icon src={iconRight} theme="outline" class="h-4 w-4" />{/if}
    </button>
{/if}
