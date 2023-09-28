<script lang="ts">
    import { _ } from "svelte-i18n";

    export let description: string | undefined;
    export let readonly = false;
</script>

<div class="w-full">
    <textarea
        class="w-full rounded-lg border border-border p-2"
        rows="5"
        name="description"
        id="description"
        bind:value={description}
        placeholder={$_("task-screen.description")}
        {readonly}
    />
</div>
