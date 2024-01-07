// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023, 2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
    WorkspaceBoardDetail,
    WorkspaceBoardSection,
    WorkspaceBoardSectionWithTasks,
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
    | {
          kind: "deleteWorkspaceBoardSection";
          workspaceBoardSection: WorkspaceBoardSection;
      }
    | { kind: "deleteTask"; task: Task }
    // XXX this is never used
    | { kind: "deleteSelectedTasks"; tasks: Task[] }
    | { kind: "archiveWorkspaceBoard"; workspaceBoard: WorkspaceBoard }
    | { kind: "deleteWorkspaceBoard"; workspaceBoard: WorkspaceBoard };

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
          location: "task";
          // TODO remove this property
          workspaceBoardSection: WorkspaceBoardSection;
      }
    | {
          kind: "task";
          task: TaskWithWorkspaceBoardSection;
          location: "dashboard";
          // TODO remove this property?
          workspaceBoardSection: WorkspaceBoardSectionWithTasks;
          workspaceBoard: WorkspaceBoardDetail;
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
    | { kind: "createWorkspaceBoardSection"; workspaceBoard: WorkspaceBoard }
    | {
          kind: "updateWorkspaceBoardSection";
          workspaceBoardSection: WorkspaceBoardSection;
      }
    | { kind: "createWorkspace" }
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

// TODO users of this type should use FormViewState (see below) instead
export type EditableViewState =
    | { kind: "viewing" }
    | { kind: "editing" }
    | { kind: "saving" };

// TODO rename FormViewState
export type AuthViewState =
    | { kind: "start" }
    | { kind: "submitting" }
    | { kind: "error"; message: string };
