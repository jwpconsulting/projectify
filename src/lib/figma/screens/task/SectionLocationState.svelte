<script lang="ts">
    export let label: string;
    export let action: (() => void) | undefined = undefined;

    $: disabled = !action;
</script>

<button
    on:click={action}
    {disabled}
    class="rounded-lg border border-transparent bg-task-hover p-2 text-xs font-bold {disabled
        ? ''
        : 'hover:bg-task-pressed focus:border-border-focus focus:bg-background focus:outline-none active:bg-secondary-hover'}"
>
    {label}
</button>
