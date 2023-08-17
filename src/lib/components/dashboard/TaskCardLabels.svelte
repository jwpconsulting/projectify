<script lang="ts">
    import { _ } from "svelte-i18n";

    import LabelList from "$lib/components/dashboard/LabelList.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
</script>

{#if task.labels.length}
    <LabelList editable={false} labels={task.labels} />
{:else}
    <div class="p-0.5">
        <div
            class="flex flex-row items-center rounded-xl border border-dashed border-primary px-4 py-1"
        >
            <button
                class="text-xxs font-bold text-primary"
                on:click|stopPropagation={console.error.bind(
                    null,
                    "not implemented"
                )}>{$_("add-label")}</button
            >
        </div>
    </div>
{/if}
