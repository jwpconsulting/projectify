import type {
    WorkspaceUserAssignment,
    LabelAssignment,
} from "$lib/types/stores";
import type {
    Label,
    Task,
    TaskWithWorkspaceBoardSection,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

// TODO rename LabelFilterInput
export type LabelSelectionInput =
    | { kind: "noLabel" }
    | { kind: "allLabels" }
    | { kind: "label"; labelUuid: string };

// TODO rename LabelFilterState
export type LabelSelection =
    | { kind: "noLabel" }
    | { kind: "allLabels" }
    | { kind: "labels"; labelUuids: Set<string> };

export type LabelAssignmentInput = LabelSelectionInput & {
    kind: "noLabel" | "label";
};
export type LabelAssignmentState = LabelSelection & {
    kind: "noLabel" | "labels";
};

// Rename WorkspaceUserFilterInput
export type WorkspaceUserSelectionInput =
    | { kind: "workspaceUser"; workspaceUser: WorkspaceUser }
    | { kind: "allWorkspaceUsers" }
    | { kind: "unassigned" };
// Rename WorkspaceUserFilterState
export type WorkspaceUserSelection =
    | { kind: "workspaceUsers"; workspaceUserUuids: Set<string> }
    | { kind: "allWorkspaceUsers" }
    | { kind: "unassigned" };

export type WorkspaceUserAssignmentInput = WorkspaceUserSelectionInput & {
    kind: "workspaceUser" | "unassigned";
};
export type WorkspaceUserAssignmentState =
    | { kind: "workspaceUser"; workspaceUser: WorkspaceUser }
    | { kind: "unassigned" };

export interface TasksPerUser {
    unassigned: number;
    assigned: Map<string, number>;
}

export type DestructiveOverlayType =
    | { kind: "deleteLabel"; label: Label }
    | { kind: "deleteWorkspaceUser"; workspaceUser: WorkspaceUser }
    // TODO rename deleteWorkspaceBoardSection
    | { kind: "deleteSection"; workspaceBoardSection: WorkspaceBoardSection }
    | { kind: "deleteTask"; task: Task }
    // XXX this is never used
    | { kind: "deleteSelectedTasks"; tasks: Task[] }
    // TODO rename archiveWorkspaceBoard
    | { kind: "archiveBoard"; workspaceBoard: WorkspaceBoard }
    // TODO rename deleteWorkspaceBoard
    | { kind: "deleteBoard"; workspaceBoard: WorkspaceBoard };

// These are the times when a header element is shown and a hamburger menu is
// needed
export type MobileMenuType =
    | { kind: "landing" }
    | { kind: "dashboard" }
    | { kind: "continue" };

export type OverlaySuccess = "success" | "rejected";

export type Overlay<Target, Anchor = void> =
    | { kind: "hidden" }
    | ({
          kind: "visible";
          target: Target;
          resolve: () => void;
          reject: (error: Error) => void;
      } & (Anchor extends HTMLElement
          ? {
                anchor: Anchor;
            }
          : object));

// TODO we could define some kind of UBER overlay type that also has a
// reference to the container, ... some time in the future Justus 2023-04-04
export type DestructiveOverlayState = Overlay<DestructiveOverlayType>;

export type MobileMenuState = Overlay<MobileMenuType>;

export type ContextMenuType =
    | { kind: "profile" }
    | { kind: "workspace"; workspaces: Workspace[] }
    | { kind: "sideNav"; workspace: Workspace }
    | { kind: "workspaceBoard"; workspaceBoard: WorkspaceBoard }
    | {
          kind: "workspaceBoardSection";
          workspaceBoard: WorkspaceBoard;
          workspaceBoardSection: WorkspaceBoardSection;
      }
    | {
          kind: "task";
          task: TaskWithWorkspaceBoardSection;
          location: "dashboard" | "task";
          workspaceBoardSection: WorkspaceBoardSection;
      }
    | { kind: "help" }
    | { kind: "permissions" }
    | {
          kind: "updateWorkspaceUser";
          workspaceUserAssignment: WorkspaceUserAssignment;
      }
    | {
          kind: "updateLabel";
          labelAssignment: LabelAssignment;
      };
// This is already pretty convoluted, so I shall go no further than this for
// now Justus 2023-08-31
export type ContextMenuState = Overlay<ContextMenuType, HTMLElement>;

export type ConstructiveOverlayType =
    | { kind: "updateWorkspaceBoard"; workspaceBoard: WorkspaceBoard }
    | { kind: "createWorkspaceBoard"; workspace: Workspace }
    | { kind: "inviteWorkspaceUser"; workspace: Workspace }
    | { kind: "inviteWorkspaceUserError"; workspace: Workspace }
    | { kind: "createWorkspaceBoardSection"; workspaceBoard: WorkspaceBoard }
    | { kind: "createWorkspace" }
    | { kind: "skipOnboarding" }
    | { kind: "recoverWorkspaceBoard"; workspaceBoard: WorkspaceBoard };
export type ConstructiveOverlayState = Overlay<ConstructiveOverlayType>;

// TODO These can probably stay in their individual svelte pages
export interface FeatureDescription {
    image: {
        position: "left" | "right";
        src: string;
        alt: string;
    };
    title: string;
    text: string;
}

export interface SolutionsHeroContent {
    title: string;
    text?: string;
    image?: {
        src: string;
        alt: string;
    };
}

export interface SolutionsPageContent {
    heroContent: SolutionsHeroContent;
    features: FeatureDescription[];
}
// END TODO

export type EditableViewState =
    | { kind: "viewing" }
    | { kind: "editing" }
    | { kind: "saving" };
