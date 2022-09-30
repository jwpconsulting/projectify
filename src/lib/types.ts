/**
 * Can be made globally available by placing this
 * inside `global.d.ts` and removing `export` keyword
 */
import type { TimestampedType, TitleDescriptionType } from "$lib/types/base";
import type {
    Label,
    WorkspaceUser,
    Task,
    WorkspaceBoardSection,
    WorkspaceBoard,
} from "$lib/types/workspace";

export interface Locals {
    userid: string;
}

export type Input = {
    name?: string;
    label?: string;
    type?: string;
    value?: any;
    error?: string;
    placeholder?: string;
    readonly?: boolean;
    selectOptions?: { label: string; value: any }[];
    validation?: {
        required?: boolean;
        validator?: (
            value: any,
            data: any
        ) => {
            error?: boolean;
            message?: string;
        };
        // Todo:
        // min?: number;
        // max?: number;
        // minLength?: number;
        // maxLength?: number;
        // pattern?: string;
    };
};

export type Workspace = {
    picture?: string;
    workspace_users?: WorkspaceUser[];
    workspace_boards?: WorkspaceBoard[];
    labels?: Label[];
    uuid: string;
} & TimestampedType &
    TitleDescriptionType;

export type ThemeColors = {
    "primary": string;
    "primary-focus": string;
    "primary-content": string;
    "secondary": string;
    "secondary-focus": string;
    "secondary-content": string;
    "accent": string;
    "accent-focus": string;
    "accent-content": string;
    "neutral": string;
    "neutral-focus": string;
    "neutral-content": string;
    "base-100": string;
    "base-200": string;
    "base-300": string;
    "base-content": string;
    "info": string;
    "success": string;
    "warning": string;
    "error": string;
};

export type Color = {
    h: number;
    s: number;
    l: number;
    br: boolean;
    style: string;
};

export type LabelSelectionInput =
    | { kind: "noLabel" }
    | { kind: "allLabels" }
    | { kind: "label"; labelUuid: string };

export type LabelSelection =
    | { kind: "noLabel" }
    | { kind: "allLabels" }
    | { kind: "labels"; labelUuids: Set<string> };

export type WorkspaceUserSelectionInput =
    | { kind: "workspaceUser"; workspaceUser: WorkspaceUser }
    | { kind: "allWorkspaceUsers" }
    | { kind: "unassigned" };
export type WorkspaceUserSelection =
    | { kind: "workspaceUsers"; workspaceUserUuids: Set<string> }
    | { kind: "allWorkspaceUsers" }
    | { kind: "unassigned" };

export type DestructiveOverlayType =
    | { kind: "deleteLabel"; label: Label }
    | { kind: "deleteMember"; workspaceUser: WorkspaceUser }
    | { kind: "deleteSection"; workspaceBoardSection: WorkspaceBoardSection }
    | { kind: "deleteTask"; task: Task }
    | { kind: "deleteSelectedTasks"; tasks: Task[] }
    | { kind: "archiveBoard"; workspaceBoard: WorkspaceBoard }
    | { kind: "deleteBoard"; workspaceBoard: WorkspaceBoard };

export type DestructiveOverlayAction =
    | { kind: "async"; action: () => Promise<void> }
    | { kind: "sync"; action: () => void };
export type DestructiveOverlayState =
    | { kind: "hidden" }
    | {
          kind: "visible";
          target: DestructiveOverlayType;
          action: DestructiveOverlayAction;
      };

export type ContextMenuType =
    | { kind: "profile" }
    | { kind: "workspace" }
    | { kind: "sideNav"; workspace: Workspace }
    | { kind: "workspaceBoard"; workspaceBoard: WorkspaceBoard }
    | {
          kind: "workspaceBoardSection";
          workspaceBoardSection: WorkspaceBoardSection;
      }
    | { kind: "task"; task: Task; location: "dashboard" }
    | { kind: "task"; task: Task; location: "task" }
    | { kind: "help" }
    | { kind: "permissions" };
export type ContextMenuState =
    | { kind: "hidden" }
    | { kind: "visible"; target: ContextMenuType; anchor: HTMLElement };

export type ConstructiveOverlayType =
    | { kind: "updateWorkspaceBoard"; workspaceBoard: WorkspaceBoard }
    | { kind: "createWorkspaceBoard"; workspace: Workspace }
    | { kind: "inviteTeamMembers"; workspace: Workspace }
    | { kind: "inviteTeamMembersNoSeatsLeft"; workspace: Workspace }
    | { kind: "createWorkspaceBoardSection"; workspaceBoard: WorkspaceBoard }
    | { kind: "createWorkspace" }
    | { kind: "skipOnboarding" }
    | { kind: "recoverWorkspaceBoard"; workspaceBoard: WorkspaceBoard };
export type ConstructiveOverlayState =
    | { kind: "hidden" }
    | { kind: "visible"; target: ConstructiveOverlayType };
