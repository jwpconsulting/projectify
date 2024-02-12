<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
    // TODO rename WorkspaceUserDropdownClosedNav
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import {
        selectedWorkspaceUser,
        filterByWorkspaceUser,
        unfilterByWorkspaceUser,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard/workspaceUserFilter";
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="workspaceUser"
        action={{ kind: "button", action: toggleUserExpandOpen }}
        active={$selectedWorkspaceUser.kind === "workspaceUsers"}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectUserClosedNav
                user={undefined}
                active={$selectedWorkspaceUser.kind === "unassigned"}
                on:select={() => filterByWorkspaceUser({ kind: "unassigned" })}
                on:deselect={() =>
                    unfilterByWorkspaceUser({ kind: "unassigned" })}
            />
            {#each $workspaceUserSearchResults as workspaceUser}
                <SelectUserClosedNav
                    user={workspaceUser.user}
                    active={$selectedWorkspaceUser.kind === "workspaceUsers" &&
                        $selectedWorkspaceUser.workspaceUserUuids.has(
                            workspaceUser.uuid,
                        )}
                    on:select={() =>
                        filterByWorkspaceUser({
                            kind: "workspaceUser",
                            workspaceUser,
                        })}
                    on:deselect={() =>
                        unfilterByWorkspaceUser({
                            kind: "workspaceUser",
                            workspaceUser,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
