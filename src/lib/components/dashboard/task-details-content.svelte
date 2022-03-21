<script lang="ts">
    import { currenTaskDetailsUUID } from "$lib/stores/dashboard";

    import { _ } from "svelte-i18n";

    import Subtasks from "./task-details-subtasks.svelte";

    export let task;
    export let subTasks;
    export let taskModified = false;
</script>

{#if task}
    <main class="flex flex-col space-y-6 pt-4">
        <div class="flex flex-col space-y-4">
            <div class="text-xl uppercase font-bold">
                {$_("description")}
            </div>

            <textarea
                rows="6"
                class="textarea textarea-bordered resize-none leading-normal p-4"
                placeholder={$_("please-enter-a-description")}
                on:input={() => (taskModified = true)}
                bind:value={task.description}
            />
        </div>
        {#if $currenTaskDetailsUUID && subTasks}
            <Subtasks taskUUID={$currenTaskDetailsUUID} {subTasks} />
        {/if}
    </main>
{/if}
