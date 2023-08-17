<script lang="ts">
    import { getTaskUrl } from "$lib/urls";

    import SubTaskProgress from "$lib/figma/buttons/SubTaskProgress.svelte";
    import Chevrons from "$lib/figma/cards/task-card/Chevrons.svelte";
    import Labels from "$lib/figma/cards/task-card/Labels.svelte";
    import MenuButton from "$lib/figma/cards/task-card/MenuButton.svelte";
    import Title from "$lib/figma/cards/task-card/Title.svelte";
    import WorkspaceUser from "$lib/figma/cards/task-card/WorkspaceUser.svelte";
    import { createMoveTaskModule } from "$lib/stores/modules";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let tasks: Task[] | undefined = undefined;
    export let workspaceBoardSection: WorkspaceBoardSection | null = null;

    export let isFirst = false;
    export let isLast = false;

    $: moveTaskModule =
        workspaceBoardSection && tasks
            ? createMoveTaskModule(workspaceBoardSection, task, tasks)
            : undefined;
</script>

<a
    class="block rounded-llg border-2 border-transparent focus:border-base-content"
    href={getTaskUrl(task.uuid)}
>
    <div class="w-full rounded-lg border border-base-300 bg-base-100 p-2">
        <!-- Compact view (< lg)-->
        <div class="flex flex-col lg:hidden">
            <div class="flex flex-row justify-between">
                <div class="">
                    <Title {task} />
                </div>
                <div class="flex flex-row items-center gap-2 justify-self-end">
                    <Chevrons
                        {task}
                        {isFirst}
                        {isLast}
                        {workspaceBoardSection}
                    />
                    <MenuButton
                        {task}
                        {workspaceBoardSection}
                        {moveTaskModule}
                    />
                </div>
            </div>
            <div class="flex flex-row justify-between">
                <div
                    class="col-span-3 flex flex-shrink flex-row overflow-x-auto sm:col-span-4"
                >
                    <Labels {task} />
                </div>
                <div
                    class="col-span-3 flex flex-row justify-self-end sm:col-span-2"
                >
                    <div class="flex flex-row items-center gap-4">
                        <SubTaskProgress {task} />
                    </div>
                    <div class="flex flex-row items-center">
                        <WorkspaceUser {task} />
                    </div>
                </div>
            </div>
        </div>
        <!-- Wide view (lg) -->
        <div
            class="hidden w-full grid-cols-[8fr_5fr_minmax(100px,_1fr)_max-content] lg:grid"
        >
            <div class="flex flex-row items-center">
                <Title {task} />
            </div>
            <div class="flex flex-row items-center justify-start gap-6">
                <Labels {task} />
            </div>
            <SubTaskProgress {task} />
            <div class="flex flex-row items-center justify-end gap-2">
                <div class="flex flex-row items-center gap-2">
                    <WorkspaceUser {task} />
                    <div>
                        <div class="flex flex-row items-center">
                            <Chevrons
                                {task}
                                {isFirst}
                                {isLast}
                                {workspaceBoardSection}
                            />
                            <MenuButton
                                {task}
                                {workspaceBoardSection}
                                {moveTaskModule}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</a>
