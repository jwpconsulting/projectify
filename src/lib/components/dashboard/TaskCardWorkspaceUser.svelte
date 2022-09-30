<script lang="ts">
    import { assignUserToTask } from "$lib/repository/workspace";
    import type { Task } from "$lib/types";
    import type { WorkspaceUser } from "$lib/types/workspace";
    import WorkspaceUserAvatar from "$lib/components/WorkspaceUserAvatar.svelte";
    import UserPicker from "../userPicker.svelte";
    import { getDropDown } from "../globalDropDown.svelte";

    export let task: Task;

    let userPickerBtnRef: HTMLElement;

    function openUserPicker() {
        let dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.openComponent(UserPicker, userPickerBtnRef, {
            selectedUser: task.assignee,
            dispatch: async (name: string, data: { user: WorkspaceUser }) => {
                if (!dropDown) {
                    throw new Error("Expected dropDown");
                }
                if (name == "userSelected") {
                    const userEmail = data.user.user
                        ? data.user.user.email
                        : null;
                    await assignUserToTask(userEmail, task.uuid);
                }
                dropDown.close();
            },
        });
    }
</script>

{#if task.assignee}
    <WorkspaceUserAvatar size={24} workspaceUser={task.assignee} />
{:else}
    <button
        bind:this={userPickerBtnRef}
        on:click|stopPropagation={() => openUserPicker()}
    >
        <WorkspaceUserAvatar workspaceUser={"assign"} size={24} />
    </button>
{/if}
