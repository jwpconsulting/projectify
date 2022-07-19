<script lang="ts">
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { _ } from "svelte-i18n";
    import { getWorkspace } from "$lib/repository";
    import Loading from "./loading.svelte";
    import UserProfilePicture from "./userProfilePicture.svelte";
    import { createEventDispatcher } from "svelte";
    import { user } from "$lib/stores/user";
    import type { Workspace, WorkspaceUser } from "$lib/types";
    import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";

    import Fuse from "fuse.js";
    import SearchInput from "./search-input.svelte";
    import { fuseSearchThreshold } from "$lib/stores/dashboard";

    export let workspaceUuid: string | null = null;
    export let selectedUser: WorkspaceUser | null | "unassigned" = null;
    export let enableUnassignedSelection = false;

    export let dispatch = createEventDispatcher();

    let workspace: Workspace | null = null;
    let loading = true;
    let workspaceWSStore: WSSubscriptionStore | null;
    let workspace_users: WorkspaceUser[] = [];

    async function fetch() {
        if (!workspaceUuid) {
            throw new Error("Expected workspaceUuid");
        }
        workspace = await getWorkspace(workspaceUuid);
        loading = false;
    }

    const refetch = debounce(() => {
        fetch();
    }, 100);

    $: {
        if (workspaceUuid) {
            fetch();

            workspaceWSStore = getSubscriptionForCollection(
                "workspace",
                workspaceUuid
            );
        }
    }

    $: {
        if ($workspaceWSStore) {
            refetch();
        }
    }

    $: {
        if (workspace) {
            if (workspace.workspace_users) {
                workspace_users = workspace.workspace_users;
            }
        }
    }

    let searchText = "";
    let searchEngine: Fuse<WorkspaceUser> | null = null;
    let filteredWorkspaceUsers: WorkspaceUser[] = [];
    $: {
        searchEngine = new Fuse(workspace_users, {
            keys: ["user.email", "user.full_name"],
            threshold: fuseSearchThreshold,
        });
    }

    $: {
        if (searchText.length) {
            if (!searchEngine) {
                throw new Error("Expected searchEngine");
            }
            filteredWorkspaceUsers = searchEngine
                .search(searchText)
                .map((res: Fuse.FuseResult<WorkspaceUser>) => res.item);
        } else {
            filteredWorkspaceUsers = workspace_users;
        }
    }

    function selectUser(user: WorkspaceUser | "unassigned" | null) {
        selectedUser = user;
        dispatch("userSelected", { user });
    }

    let searchFieldEl: HTMLElement;

    $: {
        if (searchFieldEl) {
            searchFieldEl.focus();
        }
    }

    function selectMe() {
        // find self in workspace_users
        const self = workspace_users.find((el) =>
            $user ? el.user.email == $user.email : false
        );
        if (!self) {
            throw new Error("Expected self");
        }
        selectUser(self);
    }

    function clearSelection() {
        selectUser(null);
    }

    function onBlur(event: FocusEvent) {
        const currentTarget = event.currentTarget;
        const relatedTarget = event.relatedTarget;
        if (
            currentTarget instanceof HTMLElement &&
            relatedTarget instanceof HTMLElement
        ) {
            if (!currentTarget.contains(relatedTarget)) {
                dispatch("blur");
            }
        } else {
            throw new Error("Expected HTMLElement");
        }
    }

    let rootEl: HTMLElement;
</script>

<div
    class="w-full overflow-hidden rounded-xl bg-base-100 shadow-lg"
    tabindex="-1"
    bind:this={rootEl}
    on:blur={onBlur}
>
    {#if loading}
        <div class="flex h-full w-full items-center justify-center py-8">
            <Loading />
        </div>
    {:else}
        <div class="p-4">
            <SearchInput
                placeholder={$_("search-team-member")}
                bind:inputElement={searchFieldEl}
                bind:searchText
                on:blur={() => rootEl.focus()}
            />
        </div>
        <div class="px-4 font-bold">Team Members</div>
        <ul
            class="menu flex max-h-full flex-col divide-y divide-base-300 overflow-y-auto pt-2"
        >
            {#each filteredWorkspaceUsers as workspaceUser}
                <li>
                    <a
                        class:active={selectedUser &&
                            selectedUser !== "unassigned" &&
                            selectedUser.user.email ==
                                workspaceUser.user.email}
                        class="flex flex-row space-x-4"
                        href="/"
                        on:click|preventDefault={(_) => {
                            selectUser(workspaceUser);
                        }}
                    >
                        <UserProfilePicture
                            pictureProps={{
                                url: workspaceUser.user.profile_picture,
                                size: 42,
                            }}
                        />

                        <div class="flex grow flex-col justify-start">
                            <div class="text-xs">Interface designer</div>
                            <div class="font-bold">
                                {workspaceUser.user.full_name
                                    ? workspaceUser.user.full_name
                                    : workspaceUser.user.email}
                            </div>
                        </div>
                    </a>
                </li>
            {/each}

            {#if enableUnassignedSelection}
                <li>
                    <a
                        class:active={selectedUser == "unassigned"}
                        class="flex flex-row space-x-4"
                        href="/"
                        on:click|preventDefault={(_) => {
                            selectUser("unassigned");
                        }}
                    >
                        <div
                            class="flex grow flex-col items-center justify-center"
                        >
                            <div class="font-bold">
                                {$_("assigned-to-nobody")}
                            </div>
                        </div>
                    </a>
                </li>
            {/if}
        </ul>
        <footer
            class="min-h-8 flex divide-x divide-base-300 border-t border-base-300"
        >
            {#if selectedUser}
                <div
                    class="footer-btn flex h-8 grow items-center justify-center text-primary"
                    on:click={clearSelection}
                >
                    <div class="text-xs ">{$_("clear-selection")}</div>
                </div>
                {#if selectedUser !== "unassigned"}
                    <div
                        class="footer-btn flex h-8 grow items-center justify-center text-primary"
                        on:click={selectMe}
                    >
                        <div class="text-xs ">{$_("select-me")}</div>
                    </div>
                {/if}
            {/if}
        </footer>
    {/if}
</div>

<style lang="scss">
    .footer-btn {
        @apply cursor-pointer;
        > * {
            @apply transition-all;
        }
        &:hover {
            @apply bg-base-200;
        }
    }
</style>
