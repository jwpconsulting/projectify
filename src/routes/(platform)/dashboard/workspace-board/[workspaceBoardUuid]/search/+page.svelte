<script lang="ts">
    import { _ } from "svelte-i18n";

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    $: tasks = data.tasks;
    $: search = data.search;
</script>

{#if tasks.length}
    <div class="px-4 py-6">
        <p class="text-xl font-bold">
            {$_("dashboard.showing-results-for-search", {
                values: { search },
            })}
        </p>
    </div>
    <div class="flex flex-col p-2">
        {#each tasks as task}
            <TaskCard {task} />
        {/each}
    </div>
{:else}
    <div class="flex items-center justify-center py-6">
        <div class="rounded-md bg-base-100 p-6 font-bold shadow-sm">
            {$_("dashboard.tasks-not-found-for", {
                values: { search },
            })}
        </div>
    </div>
{/if}
