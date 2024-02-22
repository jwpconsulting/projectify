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
    import { _ } from "svelte-i18n";

    import WorkspaceUserCard from "$lib/figma/screens/workspace-settings/WorkspaceUserCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { uninviteUser } from "$lib/repository/workspace";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import {
        currentWorkspaceUserCan,
        currentWorkspaceUsers,
    } from "$lib/stores/dashboard/workspaceUser";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";

    import type { PageData } from "./$types";

    export let data: PageData;

    $: workspace = $currentWorkspace ?? data.workspace;

    async function inviteWorkspaceUser() {
        await openConstructiveOverlay({
            kind: "inviteWorkspaceUser",
            workspace,
        });
    }

    async function uninvite(email: string) {
        const result = await uninviteUser(workspace, email, { fetch });
        if (result.ok) {
            return;
        }
        throw Error(JSON.stringify(result.error));
    }
</script>

<div class="flex flex-col gap-4">
    {#if $currentWorkspaceUserCan("create", "workspaceUserInvite")}
        <Button
            action={{
                kind: "button",
                action: inviteWorkspaceUser,
            }}
            label={$_(
                "workspace-settings.workspace-users.invite-new-workspace-users",
            )}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
        />
    {/if}
</div>
<section class="flex flex-col gap-4">
    <h2 class="text-xl font-bold">
        {$_("workspace-settings.workspace-users.title")}
    </h2>
    <table class="grid w-full grid-cols-4 items-center gap-y-4">
        <thead class="contents">
            <tr class="contents">
                <th
                    class="col-span-2 border-b border-border text-left font-bold"
                    >{$_(
                        "workspace-settings.workspace-users.workspace-user",
                    )}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_("workspace-settings.workspace-users.role")}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_(
                        "workspace-settings.workspace-users.actions.action",
                    )}</th
                >
            </tr>
        </thead>
        <tbody class="contents">
            {#each $currentWorkspaceUsers as workspaceUser}
                <WorkspaceUserCard {workspaceUser} />
            {:else}
                <td class="col-span-4">
                    {$_(
                        "workspace-settings.workspace-users.no-workspace-users-found",
                    )}
                </td>
            {/each}
        </tbody>
    </table>
</section>
<section class="flex flex-col gap-4">
    <h2 class="text-xl font-bold">
        {$_("workspace-settings.workspace-users.invites.title")}
    </h2>
    <table class="grid w-full grid-cols-3 items-center gap-y-4">
        <thead class="contents">
            <tr class="contents">
                <th class="border-b border-border text-left font-bold"
                    >{$_(
                        "workspace-settings.workspace-users.invites.email",
                    )}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_(
                        "workspace-settings.workspace-users.invites.date",
                    )}</th
                >
                <th class="border-b border-border text-left font-bold"
                    >{$_(
                        "workspace-settings.workspace-users.actions.action",
                    )}</th
                >
            </tr>
        </thead>
        <tbody class="contents">
            {#each workspace.workspace_user_invites as invite}
                <td class="overflow-x-auto">
                    {invite.email}
                </td>
                <td>n/a</td>
                <td
                    ><Button
                        style={{ kind: "tertiary" }}
                        color="red"
                        action={{
                            kind: "button",
                            action: uninvite.bind(null, invite.email),
                        }}
                        size="medium"
                        label={$_(
                            "workspace-settings.workspace-users.actions.uninvite",
                        )}
                        grow={false}
                    />
                </td>
            {:else}
                <td class="col-span-3">
                    {$_("workspace-settings.workspace-users.invites.empty")}
                </td>
            {/each}
        </tbody>
    </table>
</section>
<hr />
<section class="flex flex-col gap-2">
    <strong>{$_("workspace-settings.workspace-users.help.title")}</strong>
    <ul class="flex list-inside list-disc flex-col gap-2">
        <li>
            <Anchor
                href="/help/workspace-users"
                label={$_(
                    "workspace-settings.workspace-users.help.about-workspace-users",
                )}
                size="normal"
            />
        </li>
        <li>
            <Anchor
                href="/help/roles"
                label={$_(
                    "workspace-settings.workspace-users.help.about-roles",
                )}
                size="normal"
            />
        </li>
    </ul>
</section>
