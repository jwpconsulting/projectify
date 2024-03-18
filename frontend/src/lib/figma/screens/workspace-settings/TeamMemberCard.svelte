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
        deleteTeamMember,
        updateTeamMember,
    } from "$lib/repository/workspace/teamMember";
    import {
        currentTeamMember,
        currentTeamMemberCan,
    } from "$lib/stores/dashboard/teamMember";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import { teamMemberRoles } from "$lib/types/teamMemberRole";
    import type { EditableViewState } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";
    import type { TeamMember, TeamMemberRole } from "$lib/types/workspace";
    import { getMessageNameForRole } from "$lib/utils/i18n";

    export let teamMember: TeamMember;

    let preferredName: string;
    $: preferredName = getDisplayName(teamMember.user);
    let jobTitle: string;
    $: jobTitle =
        teamMember.job_title ??
        $_("workspace-settings.team-members.no-job-title");
    let role: string;
    $: role = getMessageNameForRole($_, teamMember.role);

    let mode: EditableViewState = { kind: "viewing" };

    let roleSelected: TeamMemberRole | undefined = undefined;

    async function removeUser() {
        await openDestructiveOverlay({
            kind: "deleteTeamMember",
            teamMember,
        });
        // TODO: Do something with the result
        await deleteTeamMember(teamMember, { fetch });
    }

    function startEdit() {
        mode = { kind: "editing" };
        roleSelected = teamMember.role;
    }

    async function changeRole() {
        if (roleSelected === undefined) {
            throw new Error("Expected roleSelected");
        }
        console.debug(roleSelected);
        mode = { kind: "saving" };
        await updateTeamMember(
            { ...teamMember, role: roleSelected },
            { fetch },
        );
        mode = { kind: "viewing" };
    }
    $: isCurrentUser = teamMember.uuid === $currentTeamMember?.uuid;
</script>

<tr class="contents">
    <td class="col-span-2 flex flex-row items-center gap-2">
        <AvatarVariant
            content={{ kind: "single", user: teamMember.user }}
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
            {#if $currentTeamMemberCan("update", "teamMember")}
                <CircleIcon
                    icon="edit"
                    size="medium"
                    ariaLabel={isCurrentUser
                        ? $_("workspace-settings.team-members.edit-role.self")
                        : $_(
                              "workspace-settings.team-members.edit-role.label",
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
                {#each teamMemberRoles as teamMemberRole}
                    <option value={teamMemberRole}>
                        {getMessageNameForRole($_, teamMemberRole)}
                    </option>
                {/each}
            </select>
        {:else}
            {$_("workspace-settings.team-members.edit-role.saving")}
        {/if}
    </td>
    <td
        >{#if $currentTeamMemberCan("delete", "teamMember")}<Button
                label={$_("workspace-settings.team-members.actions.remove")}
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
