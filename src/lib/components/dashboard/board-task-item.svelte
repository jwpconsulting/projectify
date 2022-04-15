<script lang="ts">
    import type { DashboardSectionsLayout } from "$lib/stores/dashboard-ui";
    import { getColorFromInx } from "$lib/utils/colors";
    import { dateStringToLocal } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import { _ } from "svelte-i18n";
    import IconPlus from "../icons/icon-plus.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import LabelList from "./labelList.svelte";

    export let layout: DashboardSectionsLayout;
    export let task = null;
    export let showHoverRing = true;

    const dispatch = createEventDispatcher();
</script>

{#if task}
    <div
        class:item-layout-grid={layout == "grid"}
        class:item-layout-list={layout == "list"}
        class="drag-handle item"
        class:hover:ring={showHoverRing}
        on:click={() => dispatch("click")}
    >
        {#if task.assignee}
            <UserProfilePicture
                pictureProps={{
                    url: task.assignee.profilePicture,
                    size: 44,
                }}
            />
        {/if}
        <div class="flex max-h-full grow flex-col overflow-y-hidden">
            {#if task.labels.length || task.deadline}
                <div
                    class="my-1 mb-2 flex items-center space-x-2 border-b border-base-300 pb-3"
                >
                    {#if task.labels.length}
                        <div class="flex grow items-center space-x-1">
                            {#if layout == "list"}
                                <LabelList
                                    size={"sm"}
                                    editable={false}
                                    labels={task.labels}
                                />
                            {:else}
                                {#each task.labels as label}
                                    <div
                                        style={`--color:${
                                            getColorFromInx(label.color).style
                                        };`}
                                        class="label-dot h-2 w-2 rounded-full"
                                    />
                                {/each}
                            {/if}
                        </div>
                    {/if}
                    {#if task.deadline}
                        <div class="item-date grid h-4 items-center">
                            <span class="nowrap-ellipsis text-xs"
                                >Date {dateStringToLocal(task.deadline)}</span
                            >
                        </div>
                    {/if}
                </div>
            {/if}

            <div class="title font-bold">
                <span>{task.title}</span>
            </div>
        </div>
    </div>
{:else}
    <div
        class="add-item ignore-elements hover:ring"
        on:click={() => dispatch("click")}
    >
        <div
            class="flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-full border-2 border-dashed border-primary text-primary"
        >
            <IconPlus />
        </div>
        <div
            class="flex max-h-full flex-col overflow-y-hidden font-bold text-primary"
        >
            {$_("new-task")}
        </div>
    </div>
{/if}

<style lang="scss">
    .item,
    .add-item {
        @apply m-2 flex cursor-pointer items-center space-x-4 overflow-y-hidden rounded-lg border border-base-300 bg-base-100 py-4 px-6;
        @apply font-bold;

        &.item-layout-grid {
            @apply h-24;
            .title {
                @apply grid grow;

                span {
                    @apply overflow-hidden text-ellipsis whitespace-nowrap;
                }
            }
        }

        &.item-layout-list {
            .item-date {
                span {
                    @apply text-sm;
                }
            }
        }
    }
</style>
