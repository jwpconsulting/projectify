<script lang="ts">
    import {
        currentWorkspaceBoardUuid,
        openTaskDetails,
    } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";
    import TaskCard from "$lib/components/dashboard/TaskCard.svelte";
    import SectionHeader from "$lib/components/dashboard/SectionHeader.svelte";
    import { createEventDispatcher } from "svelte";
    import type { WorkspaceBoardSection } from "$lib/types";

    export let section: WorkspaceBoardSection;

    export let isFirst: boolean | null = null;
    export let isLast: boolean | null = null;

    const dispatch = createEventDispatcher();

    let open: boolean = true;
    let firstOpen = open;

    function toggleOpen() {
        open = !open;
        firstOpen = true;
    }

    let contentHeight = 0;
    $: openHeight = open ? contentHeight : 0;

    function switchWithPrevSection({ detail }: { detail: any }) {
        dispatch("switchWithPrevSection", detail);
    }

    function switchWithNextSection({ detail }: { detail: any }) {
        dispatch("switchWithNextSection", detail);
    }
</script>

<div
    class="layout-list section m-2 flex select-none rounded-b-2xl bg-base-100 shadow-sm"
>
    <div class="flex grow flex-col">
        <SectionHeader
            {isLast}
            {isFirst}
            {section}
            {toggleOpen}
            bind:open
            on:switchWithPrevSection={switchWithPrevSection}
            on:switchWithNextSection={switchWithNextSection}
        />
        <main style="--open-height:{openHeight}px">
            {#if firstOpen}
                <div
                    class="content min-h-16 relative w-full grow p-4"
                    bind:clientHeight={contentHeight}
                    data-uuid={section.uuid}
                >
                    {#if section.tasks}
                        <div class="flex flex-col gap-2">
                            {#each section.tasks as task, inx (task.uuid)}
                                <TaskCard
                                    workspaceBoardSection={section}
                                    {task}
                                    isFirst={inx === 0}
                                    isLast={inx === section.tasks.length - 1}
                                    on:click={() => {
                                        if (!$currentWorkspaceBoardUuid) {
                                            throw new Error(
                                                "Expected $currentWorkspaceBoardUuid"
                                            );
                                        }
                                        openTaskDetails(
                                            $currentWorkspaceBoardUuid,
                                            task.uuid
                                        );
                                    }}
                                />
                            {/each}
                        </div>
                    {/if}
                </div>
            {/if}
        </main>
    </div>
</div>

<style lang="scss">
    main {
        --open-height: 0;
        overflow: hidden;
        position: relative;
        height: var(--open-height);
        transition: height 300ms ease-in-out;
    }

    main > .content {
        transition: transform 300ms ease-in-out;
        position: absolute;
    }

    .section {
        &.layout-list {
            .content {
                @apply flex flex-col;
            }
        }
    }
</style>
