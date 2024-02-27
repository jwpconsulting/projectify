<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import {
        deleteWorkspaceUser,
        updateWorkspaceUser,
    } from "$lib/repository/workspace/workspaceUser";
    import {
        currentWorkspaceUser,
        currentWorkspaceUserCan,
    } from "$lib/stores/dashboard/workspaceUser";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import type { EditableViewState } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";
    import type {
        WorkspaceUser,
        WorkspaceUserRole,
    } from "$lib/types/workspace";
    import { workspaceUserRoles } from "$lib/types/workspaceUserRole";
    import { getMessageNameForRole } from "$lib/utils/i18n";

    export let workspaceUser: WorkspaceUser;

    let preferredName: string;
    $: preferredName = getDisplayName(workspaceUser.user);
    let jobTitle: string;
    $: jobTitle =
        workspaceUser.job_title ??
        $_("workspace-settings.workspace-users.no-job-title");
    let role: string;
    $: role = getMessageNameForRole($_, workspaceUser.role);

    let mode: EditableViewState = { kind: "viewing" };

    let roleSelected: WorkspaceUserRole | undefined = undefined;

    async function removeUser() {
        await openDestructiveOverlay({
            kind: "deleteWorkspaceUser",
            workspaceUser,
        });
        // TODO: Do something with the result
        await deleteWorkspaceUser(workspaceUser, { fetch });
    }

    function startEdit() {
        mode = { kind: "editing" };
        roleSelected = workspaceUser.role;
    }

    async function changeRole() {
        if (roleSelected === undefined) {
            throw new Error("Expected roleSelected");
        }
        console.debug(roleSelected);
        mode = { kind: "saving" };
        await updateWorkspaceUser(
            { ...workspaceUser, role: roleSelected },
            { fetch },
        );
        mode = { kind: "viewing" };
    }
    $: isCurrentUser = workspaceUser.uuid === $currentWorkspaceUser?.uuid;
</script>

<tr class="contents">
    <td class="col-span-2 flex flex-row items-center gap-2">
        <AvatarVariant
            content={{ kind: "single", user: workspaceUser.user }}
            size="medium"
        />
        <div class="flex flex-col gap-1">
            <span class="font-bold">
                {preferredName}
            </span>
            <span>{jobTitle}</span>
        </div>
    </td>
    <td class="flex flex-row items-center gap-2">
        {#if mode.kind === "viewing"}
            <span>
                {role}
            </span>
            {#if $currentWorkspaceUserCan("update", "workspaceUser")}
                <CircleIcon
                    icon="edit"
                    size="medium"
                    ariaLabel={isCurrentUser
                        ? $_(
                              "workspace-settings.workspace-users.edit-role.self",
                          )
                        : $_(
                              "workspace-settings.workspace-users.edit-role.label",
                          )}
                    action={{
                        kind: "button",
                        action: startEdit,
                        disabled: isCurrentUser,
                    }}
                />
            {/if}
        {:else if mode.kind === "editing"}
            <select bind:value={roleSelected} on:change={changeRole}>
                {#each workspaceUserRoles as workspaceUserRole}
                    <option value={workspaceUserRole}>
                        {getMessageNameForRole($_, workspaceUserRole)}
                    </option>
                {/each}
            </select>
        {:else}
            {$_("workspace-settings.workspace-users.edit-role.saving")}
        {/if}
    </td>
    <td
        >{#if $currentWorkspaceUserCan("delete", "workspaceUser")}<Button
                label={$_("workspace-settings.workspace-users.actions.remove")}
                action={{
                    kind: "button",
                    action: removeUser,
                    disabled: isCurrentUser,
                }}
                style={{
                    kind: "tertiary",
                    icon: { position: "left", icon: X },
                }}
                color="red"
                size="medium"
            />{/if}</td
    >
</tr>
