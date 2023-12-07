<script lang="ts">
    import { _ } from "svelte-i18n";

    import DueDateWarning from "$lib/figma/buttons/DueDateWarning.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let dueDate: string | undefined;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;

    // TODO show Due soon!
    export let dueSoon = false;
</script>

<div class="flex flex-row items-center gap-4">
    <InputField
        bind:value={dueDate}
        label={undefined}
        placeholder={$_("task-screen.select-due-date")}
        name="due-date"
        style={{ inputType: "date" }}
        onClick={onInteract}
        {readonly}
    />
    {#if dueSoon}
        <DueDateWarning />
    {/if}
</div>
