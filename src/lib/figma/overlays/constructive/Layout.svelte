<script lang="ts">
    export let onSubmit: (() => void) | undefined = undefined;
</script>

<div class="flex max-w-lg grow flex-col gap-10 rounded-lg bg-foreground p-8">
    <h1 class="text-center text-3xl font-bold">
        <slot name="title" />
    </h1>
    <form class="flex flex-col gap-8" on:submit|preventDefault={onSubmit}>
        <input type="submit" class="hidden" />
        <slot name="form" />
    </form>
</div>
