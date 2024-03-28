<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023, 2024 JWP Consulting GK

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
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import {
        projectExpandOpen,
        labelExpandOpen,
        toggleProjectExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard";
    import { currentUser } from "$lib/stores/user";
    import type {
        Label,
        Task,
        Workspace,
        Section,
        ProjectDetail,
        TeamMember,
        WorkspaceDetail,
        WorkspaceQuota,
    } from "$lib/types/workspace";
    import Dashboard from "$routes/(platform)/dashboard/project/[projectUuid]/+page.svelte";

    // We are cheating a bit here
    const quota: WorkspaceQuota = {
        workspace_status: "trial",
    } as WorkspaceQuota;
    const workspaceFallback: WorkspaceDetail = {
        uuid: "does-not-exist",
        title: "",
        created: "",
        picture: null,
        modified: "",
        projects: [],
        labels: [],
        team_members: [],
        team_member_invites: [],
        quota,
    };
    const projectFallback: ProjectDetail = {
        uuid: "does-not-exist",
        title: $_("onboarding.new-project.default-name"),
        modified: "",
        created: "",
        sections: [],
        workspace: workspaceFallback,
    };
    const sectionFallback: Section = {
        title: "",
        modified: "",
        created: "",
        uuid: "",
        _order: 0,
    };
    const taskFallback: Task = {
        title: "",
        modified: "",
        created: "",
        uuid: "",
        number: 1,
        labels: [],
        _order: 0,
    };
    const labelFallback: Label = {
        name: "",
        color: 0,
        uuid: "does-not-exist",
    };

    onMount(() => {
        // Ensure we have all side panels open
        if (!$projectExpandOpen) {
            toggleProjectExpandOpen();
        }
        if (!$labelExpandOpen) {
            toggleLabelDropdownClosedNavOpen();
        }
        if (!$userExpandOpen) {
            toggleUserExpandOpen();
        }
    });

    // TODO factor into an types/onboarding.ts type so that we can test this
    // in storybook
    type State =
        | {
              kind: "new-workspace";
              workspace?: Workspace;
              title: string;
          }
        | {
              kind: "new-project";
              workspace: Workspace;
              project?: ProjectDetail;
              title: string;
          }
        | {
              kind: "new-task";
              workspace: Workspace;
              project: ProjectDetail;
              sectionTitle: string;
              title: string;
          }
        | {
              kind: "new-label";
              workspace: Workspace;
              project: ProjectDetail;
              section: Section;
              task: Task;
              title: string;
          }
        | {
              kind: "assign-task";
              workspace: Workspace;
              project: ProjectDetail;
              section: Section;
              task: Task;
              label: Label;
              assignee: TeamMember;
          };

    export let state: State;

    $: workspace = {
        ...workspaceFallback,
        ...state.workspace,
        ...(state.kind === "new-workspace"
            ? {
                  title: state.title,
                  projects: [projectFallback],
              }
            : undefined),
        ...(state.kind !== "new-workspace"
            ? { projects: [project] }
            : undefined),
    } satisfies WorkspaceDetail;

    $: project = {
        ...((state.kind === "new-workspace" ? undefined : state.project) ??
            projectFallback),
        ...(state.kind === "new-project"
            ? { title: state.title, sections: [] }
            : undefined),
        ...(state.kind === "new-task"
            ? {
                  sections: [
                      {
                          ...sectionFallback,
                          title: state.sectionTitle,
                          tasks: [{ ...taskFallback, title: state.title }],
                      },
                  ],
              }
            : undefined),
        ...(state.kind === "new-label"
            ? {
                  sections: [
                      {
                          ...state.section,
                          tasks: [
                              {
                                  ...state.task,
                                  labels: [
                                      { ...labelFallback, name: state.title },
                                  ],
                              },
                          ],
                      },
                  ],
              }
            : undefined),
        ...(state.kind === "assign-task"
            ? {
                  sections: [
                      {
                          ...sectionFallback,
                          tasks: [
                              {
                                  ...state.task,
                                  labels: [state.label],
                                  assignee: state.assignee,
                              },
                          ],
                      },
                  ],
              }
            : undefined),
    } satisfies ProjectDetail;

    const width = 500;
</script>

<div class="w-fit origin-center scale-[0.6]" style:width={width * 0.6} inert>
    <div class="flex flex-col bg-foreground ring-4 ring-border" style:width>
        <div class="flex flex-row">
            <div class="max-w-xs shrink">
                <Full {workspace} />
            </div>
            <div class="min-w-0 grow">
                {#if $currentUser}
                    <Dashboard data={{ injectProject: project }} />
                {/if}
            </div>
        </div>
    </div>
</div>
