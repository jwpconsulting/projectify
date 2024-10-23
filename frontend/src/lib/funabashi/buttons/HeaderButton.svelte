<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import type { ButtonAction } from "$lib/funabashi/types";

    export let label: string;
    export let action: ButtonAction;
    const buttonClass =
        "text-base-content flex flex-row items-center gap-2 rounded-lg p-2 hover:text-primary active:text-primary";
</script>

{#if action.kind === "button"}
    <button
        on:click={action.action}
        on:keydown={action.action}
        class={buttonClass}
    >
        <div class="text-base font-bold">
            {label}
        </div>
    </button>
{:else if action.kind === "a"}
    <!-- we just ignore the dropdown case for now -->
    <a href={action.href} class={buttonClass} on:click={action.onInteract}>
        <div class="text-base font-bold">
            {label}
        </div>
    </a>
{/if}
