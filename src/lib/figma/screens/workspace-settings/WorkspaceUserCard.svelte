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
    import { X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { deleteWorkspaceUser } from "$lib/repository/workspace/workspaceUser";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import { getDisplayName } from "$lib/types/user";
    import type { WorkspaceUser } from "$lib/types/workspace";
    import { getMessageNameForRole } from "$lib/utils/i18n";

    export let workspaceUser: WorkspaceUser;

    // Rename to preferredName
    let fullName: string;
    $: fullName = getDisplayName(workspaceUser.user);
    let jobTitle: string;
    $: jobTitle =
        workspaceUser.job_title ??
        $_("workspace-settings.workspace-users.no-job-title");
    let role: string;
    $: role = getMessageNameForRole($_, workspaceUser.role);

    async function removeUser() {
        await openDestructiveOverlay({
            kind: "deleteWorkspaceUser",
            workspaceUser,
        });
        // TODO: Do something with the result
        await deleteWorkspaceUser(workspaceUser, { fetch });
    }
</script>

<tr class="contents">
    <td class="col-span-2 flex flex-row items-center gap-2">
        <AvatarVariant
            content={{ kind: "single", user: workspaceUser.user }}
            size="medium"
        />
        <div class="flex flex-col gap-1">
            <div class="text-sm font-bold text-base-content">{fullName}</div>
            <div class="text-sm text-base-content">{jobTitle}</div>
        </div>
    </td>
    <td class="text-left text-base-content">{role}</td>
    <td class=""
        ><Button
            label={$_("workspace-settings.workspace-users.actions.remove")}
            action={{ kind: "button", action: removeUser }}
            style={{ kind: "tertiary", icon: { position: "left", icon: X } }}
            color="red"
            size="medium"
        /></td
    >
</tr>
