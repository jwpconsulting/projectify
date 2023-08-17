<script lang="ts">
    import { _ } from "svelte-i18n";

    // import Label from "$lib/figma/...";
    import DueDateWarning from "$lib/figma/buttons/DueDateWarning.svelte";
    import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let date: string | null;
    export let action: (() => void) | undefined = undefined;

    // TODO show Due soon!
    export let dueSoon = false;
</script>

<div class="flex flex-row items-center gap-4">
    {#if date}
        <SectionLocationState label={date} />
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
</div>
