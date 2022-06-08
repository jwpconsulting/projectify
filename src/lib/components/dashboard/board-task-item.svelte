<script lang="ts">
    import { getColorFromInx } from "$lib/utils/colors";
    import { dateStringToLocal } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import { _ } from "svelte-i18n";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import LabelList from "./labelList.svelte";

    export let layout: "default" | "compact" = "default";
    export let task = null;
    export let showHoverRing = true;
    export let deadLineVisible = false;
    const dispatch = createEventDispatcher();
    let dropDownMenuBtnRef;
</script>

{#if task}
    <button
        class:item-layout-compact={layout == "compact"}
        class:item-layout-default={layout == "default"}
        class="drag-handle item bg-base-100 text-left dark:bg-base-300"
        class:hover:ring={showHoverRing}
        on:click={() => dispatch("click")}
        data-uuid={task.uuid}
    >
        {#if task.assignee}
            <UserProfilePicture
                pictureProps={{
                    url: task.assignee.profilePicture,
                    size: 44,
                }}
            />
        {/if}
        <div class="flex max-h-full grow flex-col overflow-hidden">
            <div class="title flex flex-row gap-2 font-bold">
                <div class="grow">
                    <span>{task.title}</span>
                </div>
                <button
                    bind:this={dropDownMenuBtnRef}
                    on:click|stopPropagation={() => {
                        dispatch("openDropDownMenu", {
                            task,
                            target: dropDownMenuBtnRef,
                        });
                    }}
                    class="btn btn-outline btn-primary btn-circle btn-xs shrink-0"
                    ><IconMenu /></button
                >
            </div>
            {#if task.labels.length || (deadLineVisible && task.deadline)}
                <div
                    class="my-1 mt-2 flex items-start space-x-2 border-t border-base-300 pt-3 dark:border-base-100"
                >
                    <div class="flex grow flex-wrap items-center gap-2">
                        {#if task.labels.length}
                            {#if layout == "compact"}
                                {#each task.labels as label}
                                    <div
                                        style={`--color:${
                                            getColorFromInx(label.color).style
                                        };`}
                                        class="label-dot h-2 w-2 rounded-full"
                                    />
                                {/each}
                            {:else}
                                <LabelList
                                    size={"sm"}
                                    editable={false}
                                    labels={task.labels}
                                />
                            {/if}
                        {/if}
                    </div>
                    {#if task.deadline && deadLineVisible}
                        <div class="item-date grid h-4 shrink-0 items-center">
                            <span class="nowrap-ellipsis text-xs"
                                >{$_("deadline")}
                                {dateStringToLocal(task.deadline)}</span
                            >
                        </div>
                    {/if}
                </div>
            {/if}
        </div>
    </button>
{:else}
    <button
        class="add-item ignore-elements hover:ring dark:bg-base-300"
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
    </button>
{/if}

<style lang="scss">
    .item,
    .add-item {
        @apply m-2 flex cursor-pointer items-start space-x-4 overflow-y-hidden rounded-lg border border-base-300 py-4 px-4;
        @apply shrink-0 font-bold;

        &.item-layout-compact {
            @apply h-24;
            .title {
                @apply grid grow;

                span {
                    @apply overflow-hidden text-ellipsis whitespace-nowrap;
                }
            }
        }

        &.item-layout-default {
            .item-date {
                span {
                    @apply text-sm;
                }
            }
        }
    }

    .add-item {
        @apply items-center;
    }
</style>
