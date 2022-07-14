<script lang="ts">
    import {
        currentWorkspaceLabels,
        currentWorkspaceUUID,
    } from "$lib/stores/dashboard";

    import { _ } from "svelte-i18n";
    import IconCheckCircle from "../icons/icon-check-circle.svelte";
    import IconChevronDown from "../icons/icon-chevron-down.svelte";

    import IconUserCirlce from "../icons/icon-user-cirlce.svelte";
    import IconXCircle from "../icons/icon-x-circle.svelte";
    import SearchInput from "../search-input.svelte";
    import UserPicker from "../userPicker.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import LabelList from "./labelList.svelte";
    import type { WorkspaceUser, Label } from "$lib/types";

    export let searchText = "";

    export let filtersOpen = false;

    export let filterLabels: Label[] = [];

    export let filterUser: WorkspaceUser | "unassigned" | null = null;

    let fitersContentHeight = 0;

    $: filterDrawerOpen = filtersOpen || filterLabels.length;
    $: filterDrawerHeight = filterDrawerOpen ? fitersContentHeight : 0;

    function onLabelsFiltersDrawerBtnClick() {
        if (filterLabels.length > 0) {
            filterLabels = [];
            filtersOpen = false;
            return;
        }
        filtersOpen = !filtersOpen;
    }

    let userPickerEl: HTMLElement;
    let userPickerOpen = false;

    function onUserSelected({ detail: { user } }) {
        userPickerOpen = false;

        if (user === null) {
            filterUser = null;
        } else {
            filterUser = user;
        }
    }

    function onBlur(event: FocusEvent) {
        const relatedTarget = event.relatedTarget;
        if (!relatedTarget) {
            throw new Error("Expected relatedTarget");
        }
        if (relatedTarget instanceof HTMLElement) {
            if (relatedTarget && !userPickerEl.contains(relatedTarget)) {
                userPickerOpen = false;
            }
        } else {
            throw new Error("Expected HTMLElement");
        }
    }
</script>

<div class="flex grow flex-col space-y-2">
    <div class="flex grow items-center gap-2 px-4">
        <SearchInput placeholder={$_("search-task")} bind:searchText />
        <button
            on:click={onLabelsFiltersDrawerBtnClick}
            class:text-primary={filterLabels.length}
            class="btn-filter btn btn-ghost"
        >
            {#if filterLabels.length > 0}
                <IconXCircle />
                <span>
                    {$_("clear-labels-filter")}
                </span>
            {:else}
                <IconCheckCircle />
                <span>{$_("filter-by-labels")}</span>
                <div
                    class:rotate-180={filtersOpen}
                    class="icon-sm transition-all"
                >
                    <IconChevronDown />
                </div>
            {/if}
        </button>
        <div class="relative">
            <button
                tabindex="0"
                class="btn-filter btn btn-ghost"
                on:click={() => (userPickerOpen = !userPickerOpen)}
            >
                {#if filterUser !== "unassigned" && filterUser !== null}
                    <UserProfilePicture
                        pictureProps={{
                            size: 16,
                            url: filterUser.user.profile_picture,
                        }}
                    />
                    <span
                        >{filterUser.user?.full_name ||
                            filterUser.user?.email}</span
                    >
                {:else if filterUser === "unassigned"}
                    <span>{$_("assigned-to-nobody")}</span>
                {:else}
                    <IconUserCirlce />
                    <span>Filter by assignee</span>
                {/if}
                <div
                    class:rotate-180={userPickerOpen}
                    class="icon-sm transition-all"
                >
                    <IconChevronDown />
                </div>
            </button>

            {#if userPickerOpen}
                <div
                    bind:this={userPickerEl}
                    on:blur|capture={onBlur}
                    tabindex="0"
                    class="absolute top-11 right-0 z-10 w-64 max-w-md"
                >
                    <UserPicker
                        workspaceUUID={$currentWorkspaceUUID}
                        selectedUser={filterUser}
                        enableUnassignedSelection={true}
                        on:userSelected={onUserSelected}
                    />
                </div>
            {/if}
        </div>
    </div>

    <div
        style={"--open-height: " + filterDrawerHeight + "px"}
        class:open={filterDrawerOpen}
        class="filters-drawer"
    >
        <div
            bind:clientHeight={fitersContentHeight}
            class="content flex p-4  pt-2"
        >
            <div class="inline-flex flex-wrap gap-2">
                <LabelList
                    size="sm"
                    editable={true}
                    labels={$currentWorkspaceLabels}
                    bind:selectedLabels={filterLabels}
                />
            </div>
        </div>
    </div>
</div>

<style lang="scss">
    .filters-drawer {
        --open-height: 0;
        overflow: hidden;
        position: relative;
        height: var(--open-height);
        transition: height 300ms ease-in-out;
        > .content {
            transition: all 300ms ease-in-out;
            position: absolute;
            opacity: 0;
        }

        &.open {
            > .content {
                opacity: 1;
                transform: translateY(0);
            }
        }
    }
</style>
