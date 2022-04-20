<script lang="ts">
    import {
        currentWorkspaceLabels,
        currentWorkspaceUUID,
    } from "$lib/stores/dashboard";
    import { UniqueFieldDefinitionNamesRule } from "graphql";

    import { _ } from "svelte-i18n";
    import IconCheckCircle from "../icons/icon-check-circle.svelte";
    import IconChevronDown from "../icons/icon-chevron-down.svelte";

    import IconClose from "../icons/icon-close.svelte";
    import IconSearch from "../icons/icon-search.svelte";
    import IconUserCirlce from "../icons/icon-user-cirlce.svelte";
    import IconXCircle from "../icons/icon-x-circle.svelte";
    import UserPicker from "../userPicker.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import LabelList from "./labelList.svelte";

    export let searchText = "";

    export let filtersOpen = false;

    export let filterLabels = [];

    export let filterUser = null;

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

    let userPickerOpen = true;

    function onUserSelected({ detail: { user } }) {
        userPickerOpen = false;

        if (user?.email == filterUser?.email) {
            filterUser = null;
        } else {
            filterUser = user;
        }
    }
</script>

<div class="flex grow flex-col space-y-2">
    <div class="flex grow flex-wrap items-center gap-2 px-4">
        <div class="relative flex grow">
            <input
                type="text"
                placeholder={$_("search-task")}
                class="input input-bordered input-sm h-10 grow pl-9"
                bind:value={searchText}
            />
            <div
                class="icon-sm absolute top-0 left-0 flex h-full w-10 items-center justify-center rounded-l-none"
            >
                <IconSearch />
            </div>

            {#if searchText}
                <button
                    class="btn btn-ghost btn-square btn-sm absolute right-0 h-full w-10 rounded-l-none"
                    on:click={() => (searchText = "")}
                >
                    <IconClose />
                </button>
            {/if}
        </div>
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
                {#if filterUser}
                    <UserProfilePicture
                        pictureProps={{
                            size: 16,
                            url: filterUser.profilePicture,
                        }}
                    />
                    <span>{filterUser.fullName || filterUser.email}</span>
                {:else}
                    <IconUserCirlce />
                    <span>Filter by assignee</span>
                {/if}
            </button>

            {#if userPickerOpen}
                <div
                    on:blur={() => (userPickerOpen = false)}
                    tabindex="0"
                    class="absolute top-11 right-0 z-10 w-64 max-w-md"
                >
                    <UserPicker
                        workspaceUUID={$currentWorkspaceUUID}
                        selectedUser={filterUser}
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
    .btn-filter {
        @apply btn-xs flex h-10 shrink-0 items-center justify-center space-x-1 border-base-300 px-3;
    }

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
