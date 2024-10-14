<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { tick } from "svelte";
    import { _ } from "svelte-i18n";

    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import SubTaskLine from "$lib/figma/screens/task/SubTaskLine.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";
    import { getSubTaskProgress } from "$lib/utils/workspace";

    export let subTaskAssignment: SubTaskAssignment;

    $: progress = getSubTaskProgress($subTaskAssignment);

    let lineContainer: HTMLElement;

    async function onEnter() {
        // TODO (nice-to-have)
        // Locate if there are sub tasks that are empty and jump to these
        // instead
        subTaskAssignment.addSubTask();
        // wait a bit
        await tick();
        // locate the last sub task input
        const inputs = lineContainer.getElementsByTagName("input");
        const last = inputs[inputs.length - 1];
        // focus on the input
        if (last === undefined) {
            throw new Error("Expected last");
        }
        last.focus();
    }
</script>

<SubTaskBar {progress} {subTaskAssignment} />
{#if $subTaskAssignment.length > 0}
    <div class="flex flex-col" bind:this={lineContainer}>
        {#each $subTaskAssignment as subTask, index}
            <SubTaskLine
                bind:subTask
                readonly={false}
                {index}
                {subTaskAssignment}
                {onEnter}
            />
        {/each}
    </div>
{:else}
    {$_("task-screen.sub-tasks.empty-state")}
{/if}
