<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    // TODO rename to just Title or maybe TaskTitle
    import { _ } from "svelte-i18n";

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    export let title: string | undefined;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;
</script>

<InputField
    name="title"
    style={{ inputType: "text" }}
    bind:value={title}
    label={undefined}
    placeholder={$_("task-screen.form.title.placeholder")}
    onClick={onInteract}
    {readonly}
    required
/>
