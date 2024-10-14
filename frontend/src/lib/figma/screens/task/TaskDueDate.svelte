<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let dueDate: string | null;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;
</script>

<div class="flex flex-row items-center gap-4">
    <InputField
        bind:value={dueDate}
        label={undefined}
        placeholder={$_("task-screen.form.due-date.placeholder")}
        name="due-date"
        style={{ inputType: "date" }}
        onClick={onInteract}
        {readonly}
    />
</div>
