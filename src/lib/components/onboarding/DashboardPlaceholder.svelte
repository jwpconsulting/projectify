<script lang="ts">
    import { onMount } from "svelte";

    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import {
        boardExpandOpen,
        labelExpandOpen,
        toggleBoardExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard";
    import type {
        Label,
        Task,
        Workspace,
        WorkspaceBoardSection,
        WorkspaceBoardDetail,
        WorkspaceUser,
    } from "$lib/types/workspace";

    import Dashboard from "../dashboard/Dashboard.svelte";

    const workspaceFallback: Workspace = {
        uuid: "does-not-exist",
        title: "",
        created: "",
        modified: "",
    };
    const workspaceBoardFallback: WorkspaceBoardDetail = {
        uuid: "does-not-exist",
        title: "",
        modified: "",
        created: "",
        workspace_board_sections: [],
        workspace: workspaceFallback,
    };
    const workspaceBoardSectionFallback: WorkspaceBoardSection = {
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
        if (!$boardExpandOpen) {
            toggleBoardExpandOpen();
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
              kind: "new-workspace-board";
              workspace: Workspace;
              workspaceBoard?: WorkspaceBoardDetail;
              title: string;
          }
        | {
              kind: "new-task";
              workspace: Workspace;
              workspaceBoard: WorkspaceBoardDetail;
              workspaceBoardSectionTitle: string;
              title: string;
          }
        | {
              kind: "new-label";
              workspace: Workspace;
              workspaceBoard: WorkspaceBoardDetail;
              workspaceBoardSection: WorkspaceBoardSection;
              task: Task;
              title: string;
          }
        | {
              kind: "assign-task";
              workspace: Workspace;
              workspaceBoard: WorkspaceBoardDetail;
              workspaceBoardSection: WorkspaceBoardSection;
              task: Task;
              label: Label;
              assignee: WorkspaceUser;
          };

    export let state: State;

    $: workspace = {
        ...(state.workspace ?? workspaceFallback),
        ...(state.kind === "new-workspace"
            ? { title: state.title }
            : undefined),
        ...(state.kind !== "new-workspace"
            ? { workspace_boards: [workspaceBoard] }
            : undefined),
    } satisfies Workspace;
    $: workspaces = [workspace];

    $: workspaceBoard = {
        ...((state.kind === "new-workspace"
            ? undefined
            : state.workspaceBoard) ?? workspaceBoardFallback),
        ...(state.kind === "new-workspace-board"
            ? { title: state.title, workspace_board_sections: [] }
            : undefined),
        ...(state.kind === "new-task"
            ? {
                  workspace_board_sections: [
                      {
                          ...workspaceBoardSectionFallback,
                          title: state.workspaceBoardSectionTitle,
                          tasks: [{ ...taskFallback, title: state.title }],
                      },
                  ],
              }
            : undefined),
        ...(state.kind === "new-label"
            ? {
                  workspace_board_sections: [
                      {
                          ...state.workspaceBoardSection,
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
                  workspace_board_sections: [
                      {
                          ...workspaceBoardSectionFallback,
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
    } satisfies WorkspaceBoardDetail;

    const width = 500;
</script>

<div class="w-fit origin-center scale-[0.6]" style:width={width * 0.6} inert>
    <div class="flex flex-col bg-foreground ring-4 ring-border" style:width>
        <div class="flex flex-row">
            <div class="max-w-xs shrink">
                <Full {workspaces} {workspace} />
            </div>
            <div class="min-w-0 grow">
                <Dashboard {workspaceBoard} />
            </div>
        </div>
    </div>
</div>
