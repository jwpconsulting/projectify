<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Pencil } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    export let description: string | null;
    export let readonly = false;
    export let onInteract: (() => void) | undefined = undefined;
</script>

<div class="flex w-full flex-row items-start gap-4">
    {#if readonly}
        <p>{description}</p>
        <button on:click|preventDefault={onInteract} type="button">
            <Icon src={Pencil} theme="outline" class="h-4 w-4" />
        </button>
    {:else}
        <textarea
            class="w-full rounded-lg border border-border p-2"
            rows="5"
            name="description"
            id="description"
            bind:value={description}
            placeholder={$_("task-screen.form.description.placeholder")}
            {readonly}
        />
    {/if}
</div>
