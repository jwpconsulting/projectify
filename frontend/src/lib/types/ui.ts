// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK
import type { TeamMemberAssignment, LabelAssignment } from "$lib/types/stores";
import type {
    Label,
    UserWorkspace,
    ProjectDetail,
    WorkspaceDetailTeamMember,
    ProjectDetailTask,
    WorkspaceDetail,
    WorkspaceDetailProject,
    TaskDetail,
    ProjectDetailSection,
    ProjectDetailAssignee,
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

// Rename TeamMemberFilterInput
export type TeamMemberSelectionInput =
    | { kind: "teamMember"; teamMember: ProjectDetailAssignee }
    | { kind: "allTeamMembers" }
    | { kind: "unassigned" };
// Rename TeamMemberFilterState
export type TeamMemberSelection =
    | { kind: "teamMembers"; teamMemberUuids: Set<string> }
    | { kind: "allTeamMembers" }
    | { kind: "unassigned" };

export type TeamMemberAssignmentInput = TeamMemberSelectionInput & {
    kind: "teamMember" | "unassigned";
};
export type TeamMemberAssignmentState =
    | { kind: "teamMember"; teamMember: ProjectDetailAssignee }
    | { kind: "unassigned" };

export interface TasksPerUser {
    unassigned: number;
    assigned: Map<string, number>;
}

export type DestructiveOverlayType =
    | { kind: "deleteLabel"; label: Label }
    | { kind: "deleteTeamMember"; teamMember: WorkspaceDetailTeamMember }
    | {
          kind: "deleteSection";
          section: ProjectDetailSection;
      }
    | { kind: "deleteTask"; task: TaskDetail | ProjectDetailTask }
    | { kind: "archiveProject"; project: WorkspaceDetailProject }
    | { kind: "deleteProject"; project: WorkspaceDetailProject };

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
    | { kind: "workspace"; workspaces: UserWorkspace[] }
    | { kind: "sideNav"; workspace: WorkspaceDetail }
    | {
          kind: "project";
          workspace: WorkspaceDetail;
          project: WorkspaceDetailProject;
      }
    | {
          kind: "section";
          project: ProjectDetail;
          section: ProjectDetailSection;
      }
    | {
          kind: "task";
          task: TaskDetail;
          location: "task";
      }
    | {
          kind: "task";
          task: ProjectDetailTask;
          location: "dashboardSearch";
          project: ProjectDetail;
      }
    | {
          kind: "task";
          task: ProjectDetailTask;
          location: "dashboard";
          // TODO remove this property?
          section: ProjectDetailSection;
          project: ProjectDetail;
      }
    | {
          kind: "updateTeamMember";
          teamMemberAssignment: TeamMemberAssignment;
      }
    | {
          kind: "updateLabel";
          labelAssignment: LabelAssignment;
      };
// This is already pretty convoluted, so I shall go no further than this for
// now Justus 2023-08-31
export type ContextMenuState = Overlay<ContextMenuType, HTMLElement>;

export type ConstructiveOverlayType =
    | { kind: "updateProject"; project: WorkspaceDetailProject }
    | { kind: "createProject"; workspace: WorkspaceDetail }
    | { kind: "createSection"; project: ProjectDetail }
    | {
          kind: "updateSection";
          section: ProjectDetailSection;
      }
    | { kind: "recoverProject"; project: WorkspaceDetailProject };
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
    learnMore?: { href: string; label: string };
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

/**
 * This should be used for form-like widgets that are read-only by default
 * and can be modified by activating them through an edit button.
 */
export type EditableViewState =
    | { kind: "viewing" }
    | { kind: "editing" }
    | { kind: "error"; message: string }
    | { kind: "saving" };

/**
 * This is used for forms that are always editable and do not have to be
 * made editable by clicking a button or similar
 */
export type FormViewState =
    | { kind: "start" }
    | { kind: "submitting" }
    | { kind: "error"; message: string };
