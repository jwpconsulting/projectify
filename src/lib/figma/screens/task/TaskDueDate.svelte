<script lang="ts">
    import { _ } from "svelte-i18n";

    import DueDateWarning from "$lib/figma/buttons/DueDateWarning.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let date: string | undefined;
    export let action: (() => void) | undefined = undefined;

    export let readonly = false;

    // TODO show Due soon!
    export let dueSoon = false;
</script>

<div class="flex flex-row items-center gap-4">
    <InputField
        bind:value={date}
        placeholder={$_("task-screen.select-due-date")}
        name="due-date"
        style={{ kind: "field", inputType: "date" }}
        onClick={action}
        {readonly}
    />
    {#if dueSoon}
        <DueDateWarning />
    {/if}
</div>
