<script lang="ts">
    import { _ } from "svelte-i18n";

    // import Label from "$lib/figma/...";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Calendar } from "@steeze-ui/heroicons";
    import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";
    import DueDateWarning from "$lib/figma/buttons/DueDateWarning.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let date: string | null;

    // TODO show Due soon!
    export let dueSoon: boolean = false;
</script>

<div class="flex flex-row items-center gap-4">
    <Icon src={Calendar} class="w-6" theme="outline" />
    {#if date}
        <SectionLocationState label={date} />
    {:else}
        <SectionLocationState label={$_("task-screen.select-due-date")} />
    {/if}
    {#if dueSoon}
        <DueDateWarning />
    {/if}
</div>
