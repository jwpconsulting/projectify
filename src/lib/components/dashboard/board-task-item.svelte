<script lang="ts">
    import { goto } from "$app/navigation";
    import { moveTaskAfter } from "$lib/graphql/api";

    import {
        copyDashboardURL,
        currentBoardSections,
        currentBoardUUID,
        currentWorkspaceUUID,
        getDashboardURL,
    } from "$lib/stores/dashboard";

    import { getColorFromInx } from "$lib/utils/colors";
    import { dateStringToLocal } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import { _ } from "svelte-i18n";
    import { getDropDown } from "../globalDropDown.svelte";
    import IconArrowExpand from "../icons/icon-arrow-expand.svelte";
    import IconArrowSDown from "../icons/icon-arrow-s-down.svelte";
    import IconArrowSRight from "../icons/icon-arrow-s-right.svelte";
    import IconArrowSUp from "../icons/icon-arrow-s-up.svelte";
    import IconChatAlt from "../icons/icon-chat-alt.svelte";
    import IconCopyLink from "../icons/icon-copy-link.svelte";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import IconSortAscending from "../icons/icon-sort-ascending.svelte";
    import IconSortDescending from "../icons/icon-sort-descending.svelte";
    import IconSwitchVertical from "../icons/icon-switch-vertical.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import LabelList from "./labelList.svelte";

    export let layout: "default" | "compact" = "default";
    export let task = null;
    export let showHoverRing = true;
    export let deadLineVisible = false;

    export let sectionUUID;

    const dispatch = createEventDispatcher();

    let dropDownMenuBtnRef;

    $: url =
        task &&
        getDashboardURL($currentWorkspaceUUID, $currentBoardUUID, task.uuid);

    let menuSectionsItems = $currentBoardSections
        .filter((section) => section.uuid != sectionUUID)
        .map((it) => {
            return {
                label: it.title,
                icon: IconArrowSRight,
                onClick: () => {
                    moveTaskAfter(task.uuid, it.uuid);
                },
            };
        });

    let dropDownItems = [
        {
            label: "Open",
            icon: IconArrowExpand,

            onClick: () => {
                goto(url);
            },
        },
        {
            label: "Move to section",
            icon: IconSwitchVertical,
            items: menuSectionsItems,
        },
        {
            label: "Move to top",
            icon: IconSortAscending,
        },
        {
            label: "Move to bottom",
            icon: IconSortDescending,
        },
        {
            label: "Move to previews position",
            icon: IconArrowSUp,
        },
        {
            label: "Move to next position",
            icon: IconArrowSDown,
        },
        {
            label: "Copy link",
            icon: IconCopyLink,
            onClick: () => {
                copyDashboardURL(
                    $currentWorkspaceUUID,
                    $currentBoardUUID,
                    task.uuid
                );
            },
        },
        {
            label: "Goto updates",
            icon: IconChatAlt,
        },
        {
            label: "Delete task",
            icon: IconTrash,
        },
    ];

    function openDropDownMenu() {
        getDropDown().open(dropDownItems, dropDownMenuBtnRef);
    }
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
            {#if task.labels.length || task.deadline}
                <div class="title flex flex-row font-bold">
                    <div class="grow">
                        <span>{task.title}</span>
                    </div>
                    <button
                        bind:this={dropDownMenuBtnRef}
                        on:click|stopPropagation={() => {
                            openDropDownMenu();
                        }}
                        class="btn btn-outline btn-primary btn-circle btn-xs shrink-0"
                        ><IconMenu /></button
                    >
                </div>
                <div
                    class="my-1 mt-2 flex items-start space-x-2 border-t border-base-300 pt-3 dark:border-base-100"
                >
                    {#if task.labels.length}
                        <div class="flex grow flex-wrap items-center gap-2">
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
                        </div>
                    {/if}
                    {#if task.deadline && deadLineVisible}
                        <div class="item-date grid h-4 shrink-0 items-center">
                            <span class="nowrap-ellipsis text-xs"
                                >Date {dateStringToLocal(task.deadline)}</span
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
