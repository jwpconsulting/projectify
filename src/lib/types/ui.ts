import type {
    Label,
    WorkspaceUser,
    Task,
    WorkspaceBoardSection,
    WorkspaceBoard,
    Workspace,
} from "$lib/types/workspace";
import type {
    WorkspaceSearchModule,
    SideNavModule,
    WorkspaceBoardSectionModule,
} from "$lib/types/stores";
import type { SvelteComponentTyped } from "svelte";

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
    };
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
export type TasksPerUser = {
    unassigned: number;
    assigned: Map<string, number>;
};

export type DestructiveOverlayType =
    | { kind: "deleteLabel"; label: Label }
    | { kind: "deleteMember"; workspaceUser: WorkspaceUser }
    | { kind: "deleteSection"; workspaceBoardSection: WorkspaceBoardSection }
    | { kind: "deleteTask"; task: Task }
    | { kind: "deleteSelectedTasks"; tasks: Task[] }
    | { kind: "archiveBoard"; workspaceBoard: WorkspaceBoard }
    | { kind: "deleteBoard"; workspaceBoard: WorkspaceBoard };

export type Overlay<Target, Action> =
    | { kind: "hidden" }
    | {
          kind: "visible";
          target: Target;
          action: Action;
      };

// XXX need typeof here for some reason
export type OverlayComponent = typeof SvelteComponentTyped<{
    // TODO this has to be something, the generic version of
    // DestructiveOverlayType
    target: any;
}>;

export type OverlayAction =
    | { kind: "async"; action: () => Promise<void> }
    | { kind: "sync"; action: () => void };

// TODO we could define some kind of UBER overlay type that also has a
// reference to the container, ... some time in the future Justus 2023-04-04
export type DestructiveOverlayState = Overlay<
    DestructiveOverlayType,
    OverlayAction
>;

export type ContextMenuType =
    | { kind: "profile" }
    | { kind: "workspace"; workspaceSearchModule: WorkspaceSearchModule }
    | { kind: "sideNav"; workspace: Workspace; sideNavModule: SideNavModule }
    | { kind: "workspaceBoard"; workspaceBoard: WorkspaceBoard }
    | {
          kind: "workspaceBoardSection";
          workspaceBoardSection: WorkspaceBoardSection;
          workspaceBoardSectionModule: WorkspaceBoardSectionModule;
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
export type ConstructiveOverlayState = Overlay<
    ConstructiveOverlayType,
    OverlayAction
>;

export type FeatureDescription = {
    image: {
        position: "left" | "right";
        src: string;
        alt: string;
    };
    header: string;
    text: string;
};

export type SolutionsHeroContent = {
    header: string;
    text: string;
    image: {
        src: string;
        alt: string;
    };
};

export type SolutionsPageContent = {
    heroContent: SolutionsHeroContent;
    features: FeatureDescription[];
};
