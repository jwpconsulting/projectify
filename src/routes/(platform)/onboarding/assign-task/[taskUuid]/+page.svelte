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

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getDashboardWorkspaceBoardUrl, getSettingsUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    export let data: PageData;

    const {
        task,
        assignee,
        workspaceBoard,
        workspaceBoardSection,
        workspace,
        label,
    } = data;

    const taskTitle = task.title;
</script>

<Onboarding
    stepCount={5}
    step={5}
    nextLabel={$_("onboarding.assign-task.continue")}
    nextAction={{
        kind: "a",
        href: getDashboardWorkspaceBoardUrl(workspaceBoard.uuid),
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.assign-task.title", {
            values: { taskTitle },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>{$_("onboarding.assign-task.prompt.finished")}</p>
            <p>{$_("onboarding.assign-task.prompt.adding-workspace-users")}</p>
            <Anchor
                href="/help/billing"
                label={$_("onboarding.assign-task.follow-up.billing-help")}
                openBlank
            />
            <Anchor
                href={getSettingsUrl(workspace.uuid, "billing")}
                label={$_(
                    "onboarding.assign-task.follow-up.go-to-billing-settings",
                )}
                openBlank
            />
        </div>
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "assign-task",
            task,
            label,
            workspace,
            workspaceBoard,
            workspaceBoardSection,
            assignee,
        }}
    />
</Onboarding>
