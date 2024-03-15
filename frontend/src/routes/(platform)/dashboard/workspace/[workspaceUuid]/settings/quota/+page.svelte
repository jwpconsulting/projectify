<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2024 JWP Consulting GK

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
<!-- @component Show quota for workspace resources. Visible to any ws user. -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import type { Quota } from "$lib/types/workspace";

    import type { PageData } from "./$types";

    export let data: PageData;
    $: workspace = $currentWorkspace ?? data.workspace;

    $: quotaRows = [
        {
            label: $_(
                "workspace-settings.quota.resource.workspace-users-and-invites",
            ),
            quota: workspace.quota.workspace_users_and_invites,
        },
        {
            label: $_("workspace-settings.quota.resource.projects"),
            quota: workspace.quota.projects,
        },
        {
            label: $_("workspace-settings.quota.resource.sections"),
            quota: workspace.quota.sections,
        },
        {
            label: $_("workspace-settings.quota.resource.tasks"),
            quota: workspace.quota.tasks,
        },
        {
            label: $_("workspace-settings.quota.resource.labels"),
            quota: workspace.quota.labels,
        },
        {
            label: $_("workspace-settings.quota.resource.sub-tasks"),
            quota: workspace.quota.sub_tasks,
        },
        {
            label: $_("workspace-settings.quota.resource.task-labels"),
            quota: workspace.quota.task_labels,
        },
    ].filter((q) => q.quota.limit !== null) satisfies {
        label: string;
        quota: Quota;
    }[];
</script>

<section class="flex flex-col gap-2">
    <p>
        <strong>{$_("workspace-settings.quota.workspace-status.label")}</strong
        >
        {#if workspace.quota.workspace_status === "full"}
            {$_("workspace-settings.quota.workspace-status.full")}
        {:else if workspace.quota.workspace_status === "trial"}
            {$_("workspace-settings.quota.workspace-status.trial")}
        {:else if workspace.quota.workspace_status === "inactive"}
            {$_("workspace-settings.quota.workspace-status.inactive")}
        {/if}
    </p>

    {#if quotaRows.length}
        <p>
            {$_("workspace-settings.quota.explanation.quota-for", {
                values: { title: workspace.title },
            })}
        </p>
        <table>
            <thead>
                <tr>
                    <th class="text-left">
                        {$_("workspace-settings.quota.columns.resource")}
                    </th>
                    <th class="text-right">
                        {$_("workspace-settings.quota.columns.current")}
                    </th>
                    <th class="text-right">
                        {$_("workspace-settings.quota.columns.limit")}
                    </th>
                </tr>
            </thead>
            <tbody>
                {#each quotaRows as quotaRow}
                    <tr>
                        <td>
                            {quotaRow.label}
                        </td>
                        <td class="text-right">
                            {#if quotaRow.quota.current === null}
                                {$_("workspace-settings.quota.rows.na")}
                            {:else}
                                {quotaRow.quota.current}
                            {/if}
                        </td>
                        <td class="text-right">
                            {#if quotaRow.quota.limit === null}
                                {$_("workspace-settings.quota.rows.unlimited")}
                            {:else}
                                {quotaRow.quota.limit}
                            {/if}
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    {:else}
        {$_("workspace-settings.quota.explanation.no-quota")}
    {/if}
</section>

<section class="flex flex-col gap-2">
    <h3 class="font-bold">
        {$_("workspace-settings.quota.help.title")}
    </h3>
    <ul class="list-inside list-disc">
        <li>
            <Anchor
                label={$_("workspace-settings.quota.help.paid")}
                href="/help/quota#paid"
                size="normal"
                openBlank
            />
        </li>
        <li>
            <Anchor
                label={$_("workspace-settings.quota.help.trial")}
                href="/help/quota#trial"
                size="normal"
                openBlank
            />
        </li>
    </ul>
</section>
