<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 Saki Adachi -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon";

    import type { MenuButtonColor } from "$lib/figma/types";
    import type { ButtonAction } from "$lib/funabashi/types";
    import { closeContextMenu } from "$lib/stores/globalUi";
    import { tw } from "$lib/utils/ui";

    export let label: string;
    export let icon: IconSource | undefined = undefined;
    export let iconRight: IconSource | undefined = undefined;
    // TODO remove default
    export let color: MenuButtonColor = "base";
    export let kind: ButtonAction & { kind: "button" | "a" };
    export let closeOnInteract = true;

    $: colorStyle = {
        base: "text-base-content",
        primary: "text-primary",
        destructive: "text-destructive",
    }[color];

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

    $: outerClass = tw`flex w-full flex-row items-center gap-2 px-4 py-2 font-bold hover:bg-secondary-hover active:bg-disabled disabled:active:bg-secondary-hover ${colorStyle}`;
</script>

{#if kind.kind === "a"}
    <a href={kind.href} class={outerClass} on:click={interact}>
        {#if icon}<Icon src={icon} theme="outline" class="h-4 w-4" />{/if}
        {label}
        {#if iconRight}
            <Icon src={iconRight} theme="outline" class="h-4 w-4" />{/if}
    </a>
{:else}
    <button disabled={kind.disabled} on:click={action} class={outerClass}>
        {#if icon}<Icon src={icon} theme="outline" class="h-4 w-4" />{/if}
        <span class="truncate">{label}</span>
        {#if iconRight}
            <Icon src={iconRight} theme="outline" class="h-4 w-4" />{/if}
    </button>
{/if}
