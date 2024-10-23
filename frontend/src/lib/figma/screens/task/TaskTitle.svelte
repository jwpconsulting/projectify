<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    // TODO rename to just Title or maybe TaskTitle
    import { _ } from "svelte-i18n";

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Pencil } from "@steeze-ui/heroicons";

    export let title: string | undefined;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;
</script>

{#if readonly}
    <div class="flex flex-row gap-4">
        {title}
        <button
            class="flex flex-row"
            on:click|preventDefault={onInteract}
            type="button"
        >
            <Icon src={Pencil} theme="outline" class="h-4 w-4" />
        </button>
    </div>
{:else}
    <InputField
        name="title"
        style={{ inputType: "text" }}
        bind:value={title}
        label={undefined}
        placeholder={$_("task-screen.form.title.placeholder")}
        onClick={onInteract}
        required
    />
{/if}
