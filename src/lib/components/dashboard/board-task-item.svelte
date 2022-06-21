<script lang="ts">
    import { getColorFromInx } from "$lib/utils/colors";
    import { dateStringToLocal } from "$lib/utils/date";
    import { createEventDispatcher } from "svelte";
    import { _ } from "svelte-i18n";
    import { assign } from "svelte/internal";
    import IconChevronDown from "../icons/icon-chevron-down.svelte";
    import IconChevronUp from "../icons/icon-chevron-up.svelte";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import ProfilePicture from "../profilePicture.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import LabelList from "./labelList.svelte";

    export let layout: "default" | "compact" = "default";
    export let task = null;
    export let showHoverRing = true;
    const dispatch = createEventDispatcher();
    let dropDownMenuBtnRef;

    export let isFirst = false;
    export let isLast = false;

    let userPickerBtnRef;
    let labelPickerBtnRef;

    function moveUp() {
        dispatch("moveUp", { task });
    }
    function moveDown() {
        dispatch("moveDown", { task });
    }
    function openUserPicker() {
        dispatch("openUserPicker", { task, target: userPickerBtnRef });
    }
    function openLabelPicker() {
        dispatch("openLabelPicker", { task, target: labelPickerBtnRef });
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
        <div class="flex max-h-full grow flex-col">
            <div class="title flex flex-row gap-2 font-bold">
                <div class="w-12 shrink-0 truncate text-sm opacity-50">
                    #{task.number}
                </div>
                <div class="grow text-sm">
                    <span>{task.title}</span>
                </div>
                <div class="flex gap-2">
                    <button
                        disabled={isFirst}
                        on:click|stopPropagation={() => moveUp()}
                        class="btn btn-primary btn-ghost btn-circle btn-xs shrink-0"
                        ><IconChevronUp /></button
                    >
                    <button
                        disabled={isLast}
                        on:click|stopPropagation={() => moveDown()}
                        class="btn btn-primary btn-ghost btn-circle btn-xs shrink-0"
                        ><IconChevronDown /></button
                    >
                    <button
                        bind:this={dropDownMenuBtnRef}
                        on:click|stopPropagation={() => {
                            dispatch("openDropDownMenu", {
                                task,
                                target: dropDownMenuBtnRef,
                            });
                        }}
                        class="btn btn-primary btn-ghost btn-circle btn-xs shrink-0"
                        ><IconMenu /></button
                    >
                </div>
            </div>

            <div
                class="mt-3 flex items-center space-x-2 border-t border-base-300 pt-4 dark:border-base-100"
            >
                {#if task.assignee}
                    <UserProfilePicture
                        pictureProps={{
                            url: task.assignee.profilePicture,
                            size: 36,
                        }}
                    />
                {:else}
                    <div bind:this={userPickerBtnRef}>
                        <ProfilePicture
                            on:click={() => openUserPicker()}
                            showPlus={true}
                            size={36}
                        />
                    </div>
                {/if}

                <div
                    class="flex grow flex-wrap items-center justify-end gap-2"
                >
                    {#if task.labels.length}
                        <LabelList
                            size={"sm"}
                            editable={false}
                            labels={task.labels}
                        />
                    {:else}
                        <button
                            bind:this={labelPickerBtnRef}
                            on:click|stopPropagation={() => openLabelPicker()}
                            class="btn-dashed">{$_("add-label")}</button
                        >
                    {/if}
                </div>
            </div>
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
