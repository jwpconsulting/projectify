<script lang="ts">
    import { _, date as formatDate } from "svelte-i18n";

    import DueDateWarning from "$lib/figma/buttons/DueDateWarning.svelte";
    import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let date: string | undefined;
    export let action: (() => void) | undefined = undefined;

    export let readonly = false;

    // TODO show Due soon!
    export let dueSoon = false;
    // XXX assumes that its valid
    $: valueAsDate = date ? new Date(date) : undefined;
</script>

<div class="flex flex-row items-center gap-4">
    {#if readonly}
        {#if valueAsDate}
            <SectionLocationState label={$formatDate(valueAsDate)} />
        {:else}
            <SectionLocationState
                label={action
                    ? $_("task-screen.select-due-date")
                    : $_("task-screen.no-due-date")}
            />
        {/if}
        {#if dueSoon}
            <DueDateWarning />
        {/if}
    {:else}
        <InputField
            bind:value={date}
            placeholder={$_("")}
            label={$_("")}
            name="due-date"
            style={{ kind: "field", inputType: "date" }}
        />
    {/if}
</div>
