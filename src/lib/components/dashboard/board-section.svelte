<script lang="ts">
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import IconChevronRight from "../icons/icon-chevron-right.svelte";
    import {
        assignUserToTask,
        copyDashboardURL,
        currentBoardSections,
        currentBoardUUID,
        currentWorkspaceUUID,
        deleteTask,
        moveTaskAfter,
        openNewTask,
        openTaskDetails,
    } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";
    import { sortable } from "$lib/actions/sortable";
    import delay from "delay";
    import { client } from "$lib/graphql/client";
    import {
        Mutation_DeleteWorkspaceBoardSection,
        Mutation_UpdateWorkspaceBoardSection,
    } from "$lib/graphql/operations";
    import ToolBar from "./toolBar.svelte";
    import { getModal } from "../dialogModal.svelte";
    import { dashboardSectionsLayout } from "$lib/stores/dashboard-ui";
    import BoardTaskItem from "./board-task-item.svelte";
    import { getDropDown } from "../globalDropDown.svelte";
    import IconArrowSRight from "../icons/icon-arrow-s-right.svelte";
    import type { DropDownMenuItem } from "../globalDropDown.svelte";
    import IconArrowExpand from "../icons/icon-arrow-expand.svelte";
    import IconSwitchVertical from "../icons/icon-switch-vertical.svelte";
    import IconSortAscending from "../icons/icon-sort-ascending.svelte";
    import IconSortDescending from "../icons/icon-sort-descending.svelte";
    import IconArrowSUp from "../icons/icon-arrow-s-up.svelte";
    import IconArrowSDown from "../icons/icon-arrow-s-down.svelte";
    import IconCopyLink from "../icons/icon-copy-link.svelte";
    import IconChatAlt from "../icons/icon-chat-alt.svelte";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconSelector from "../icons/icon-selector.svelte";
    import IconClose from "../icons/icon-close.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import { createEventDispatcher } from "svelte";
    import UserPicker from "../userPicker.svelte";
    import LabelPicker from "./labelPicker.svelte";
    import type { WorkspaceBoardSection, WorkspaceUser } from "$lib/types";

    export let section: WorkspaceBoardSection;

    export let isFirst: boolean | null = null;
    export let isLast: boolean | null = null;

    export let isDragging = false;

    const dispatch = createEventDispatcher();

    let open = true;
    let firstOpen = open;

    function toggleOpen() {
        if (isDragging) {
            return;
        }
        open = !open;
        firstOpen = true;
    }

    let contentHeght = 0;
    $: openHeight =
        open || $dashboardSectionsLayout == "columns" ? contentHeght : 0;
    $: openArrowDeg = open ? 90 : 0;

    async function onEdit() {
        let modalRes = await getModal("editBoardSectionModal").open(section);

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_UpdateWorkspaceBoardSection,
                variables: {
                    input: {
                        uuid: section.uuid,
                        title: modalRes.outputs.title,
                        description: "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onDelete() {
        let modalRes = await getModal("deleteBoardSectionConfirmModal").open();

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_DeleteWorkspaceBoardSection,
                variables: {
                    input: {
                        uuid: section.uuid,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    function taskDragStart() {
        isDragging = true;
    }

    async function taskDragEnd({ detail }) {
        if (!section.tasks) {
            throw new Error("Expected section.tasks");
        }
        await delay(10);
        isDragging = false;

        const prevUUID =
            detail.item.previousElementSibling?.getAttribute("data-uuid") ||
            null;

        let task = section.tasks[detail.oldIndex];
        const fromSectionUUID = detail.from.getAttribute("data-uuid");
        const toSectionUUID = detail.to.getAttribute("data-uuid");

        if (
            task &&
            (fromSectionUUID != toSectionUUID ||
                detail.newIndex != detail.oldIndex)
        ) {
            await moveTaskAfter(task.uuid, toSectionUUID, prevUUID);
        }
    }

    function onHandlerOver(_e: Event) {
        if (isDragging) {
            open = true;
            firstOpen = true;
        }
    }

    $: layoutClass = `layout-${$dashboardSectionsLayout}`;
    $: collapsable = $dashboardSectionsLayout != "columns";

    function openItemDropDownMenu({ detail: { task, target } }) {
        if (!section.tasks) {
            throw new Error("Expected section.tasks");
        }
        let lastTask = section.tasks[section.tasks.length - 1];
        let prevTask = section.tasks[section.tasks.indexOf(task) - 1];
        let nextTask = section.tasks[section.tasks.indexOf(task) + 1];
        let isFirst = task.uuid == section.tasks[0].uuid;
        let isLast = task.uuid == lastTask.uuid;

        let menuSectionsItems = $currentBoardSections
            .filter(
                (itSec: WorkspaceBoardSection) => itSec.uuid != section.uuid
            )
            .map((it: WorkspaceBoardSection) => {
                return {
                    label: it.title,
                    icon: IconArrowSRight,
                    onClick: () => {
                        moveTaskAfter(task.uuid, it.uuid);
                    },
                };
            });

        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("open-task"),
                icon: IconArrowExpand,

                onClick: () => {
                    openTaskDetails(task.uuid);
                },
            },
            {
                label: $_("move-to-section"),
                icon: IconSwitchVertical,
                items: menuSectionsItems,
            },
            {
                label: $_("move-to-top"),
                icon: IconSortAscending,
                hidden: isFirst === true,
                onClick: () => {
                    moveTaskAfter(task.uuid, section.uuid, null);
                },
            },
            {
                label: $_("move-to-bottom"),
                icon: IconSortDescending,
                hidden: isLast === true,
                onClick: () => {
                    moveTaskAfter(task.uuid, section.uuid, lastTask.uuid);
                },
            },
            {
                label: $_("move-to-previous-position"),
                icon: IconArrowSUp,
                hidden: isFirst === true,
                onClick: () => {
                    moveTaskAfter(task.uuid, section.uuid, prevTask?.uuid);
                },
            },
            {
                label: $_("move-to-next-position"),
                icon: IconArrowSDown,
                hidden: isLast === true,
                onClick: () => {
                    moveTaskAfter(task.uuid, section.uuid, nextTask?.uuid);
                },
            },
            {
                label: $_("copy-link"),
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
                label: $_("goto-to-updates"),
                icon: IconChatAlt,
                onClick: () => {
                    openTaskDetails(task.uuid, "updates");
                },
            },
            {
                label: $_("delete-task"),
                icon: IconTrash,
                onClick: () => {
                    deleteTask(task);
                },
            },
        ];
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, target);
    }

    let dropDownMenuBtnRef: HTMLElement;

    function openDropDownMenu() {
        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("expand-section"),
                icon: IconSelector,
                hidden: !collapsable || open,
                onClick: () => {
                    open = true;
                },
            },
            {
                label: $_("collapse-section"),
                icon: IconClose,
                hidden: !collapsable || !open,
                onClick: () => {
                    open = false;
                },
            },
            {
                label: $_("switch-with-previous-section"),
                icon: IconArrowSUp,
                hidden: isFirst === true,
                onClick: () => {
                    dispatch("switchWithPrevSection", { section });
                },
            },
            {
                label: $_("switch-with-next-section"),
                icon: IconArrowSDown,
                hidden: isLast === true,
                onClick: () => {
                    dispatch("switchWithNextSection", { section });
                },
            },
            {
                label: $_("add-task"),
                icon: IconPlus,
                onClick: () => {
                    openNewTask(section.uuid);
                },
            },
        ];
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, dropDownMenuBtnRef);
    }

    function moveUpItem({ detail: { task } }) {
        if (!section.tasks) {
            throw new Error("Expected section.tasks");
        }
        let prevTask = section.tasks[section.tasks.indexOf(task) - 1];
        moveTaskAfter(task.uuid, section.uuid, prevTask?.uuid);
    }

    function moveDownItem({ detail: { task } }) {
        if (!section.tasks) {
            throw new Error("Expected section.tasks");
        }
        let nextTask = section.tasks[section.tasks.indexOf(task) + 1];
        moveTaskAfter(task.uuid, section.uuid, nextTask?.uuid);
    }

    function openUserPicker({ detail: { task, target } }) {
        let dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.openComponent(UserPicker, target, {
            workspaceUUID: $currentWorkspaceUUID,
            selectedUser: task.assignee,
            dispatch: async (name: string, data: WorkspaceUser) => {
                if (!dropDown) {
                    throw new Error("Expected dropDown");
                }
                if (name == "userSelected") {
                    await assignUserToTask(data.user.email, task.uuid);
                }
                dropDown.close();
            },
        });
    }

    function openLabelPicker({ detail: { task, target } }) {
        let dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.openComponent(LabelPicker, target, {
            task,
            dispatch: async (_name: string, _data: any) => {
                if (!dropDown) {
                    throw new Error("Expected dropDown");
                }
                dropDown.close();
            },
        });
    }
</script>

<div
    class={`${layoutClass} section m-2 flex select-none rounded-b-2xl bg-base-100 shadow-sm`}
>
    <div class="flex grow flex-col">
        <header
            class:open={open || $dashboardSectionsLayout == "columns"}
            class="sticky -top-2 z-[2] flex h-16 cursor-pointer  select-none items-center bg-base-100 p-2"
            on:click={$dashboardSectionsLayout == "columns"
                ? null
                : toggleOpen}
            on:focus={onHandlerOver}
            on:mouseover={onHandlerOver}
        >
            {#if $dashboardSectionsLayout != "columns"}
                <div
                    class="px-2 transition-transform"
                    style="transform: rotate({openArrowDeg}deg);"
                >
                    <IconChevronRight />
                </div>
            {/if}
            <div
                class="drag-handle ml-2 grid grow cursor-move font-bold uppercase"
            >
                <span class="nowrap-ellipsis">
                    {section.title}
                    {#if !open && section.tasks} ({section.tasks.length}) {/if}
                </span>
            </div>
            {#if section.tasks}
                <ToolBar
                    items={[
                        { label: $_("Edit"), icon: IconEdit, onClick: onEdit },
                        {
                            label: $_("Delete"),
                            icon: IconTrash,
                            onClick: onDelete,
                            disabled: section.tasks.length > 0,
                            tooltip: section.tasks.length
                                ? $_("remove-section-tooltip-message")
                                : "",
                        },
                    ]}
                />
            {/if}
            <button
                bind:this={dropDownMenuBtnRef}
                on:click|stopPropagation={openDropDownMenu}
                class="btn btn-outline btn-primary btn-circle btn-xs mx-2 shrink-0"
                ><IconMenu /></button
            >
        </header>
        <main
            style="--open-height:{openHeight}px"
            class:hover:ring={isDragging}
        >
            {#if firstOpen || $dashboardSectionsLayout == "columns"}
                <div
                    class="content min-h-16 relative w-full grow p-2"
                    bind:clientHeight={contentHeght}
                    use:sortable={{ group: "Tasks" }}
                    on:dragStart={taskDragStart}
                    on:dragEnd={taskDragEnd}
                    data-uuid={section.uuid}
                >
                    {#if section.tasks}
                        {#each section.tasks as task, inx (task.uuid)}
                            <BoardTaskItem
                                {task}
                                isFirst={inx === 0}
                                isLast={inx === section.tasks.length - 1}
                                showHoverRing={!isDragging}
                                on:openDropDownMenu={openItemDropDownMenu}
                                on:moveDown={moveDownItem}
                                on:moveUp={moveUpItem}
                                on:openUserPicker={openUserPicker}
                                on:openLabelPicker={openLabelPicker}
                                on:click={() =>
                                    !isDragging && openTaskDetails(task.uuid)}
                            />
                        {/each}
                    {/if}
                    {#if !isDragging}
                        <BoardTaskItem
                            on:click={() => openNewTask(section.uuid)}
                        />
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

    :global(.sortable-ghost) {
        opacity: 0;
    }

    header {
        &::after {
            content: "";
            position: absolute;

            height: 1px;
            @apply bottom-0 left-3 right-3 bg-base-300;
            transition: all 300ms ease-in-out;
            opacity: 0;
        }

        &.open {
            &::after {
                opacity: 1;
            }
        }
    }

    .section {
        &.layout-grid {
            .content {
                @apply grid;
                grid-auto-flow: row dense;
                grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            }
        }
        &.layout-list {
            .content {
                @apply flex flex-col;
            }
        }
        &.layout-columns {
            max-height: calc(100% - 16px);
            main {
                @apply overflow-y-auto;
            }
            .content {
                @apply flex flex-col;
            }
        }
    }
</style>
