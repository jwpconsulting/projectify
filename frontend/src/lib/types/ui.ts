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
import type { TeamMemberAssignment, LabelAssignment } from "$lib/types/stores";
import type {
    Label,
    Task,
    TaskWithSection,
    Workspace,
    Project,
    ProjectDetail,
    Section,
    SectionWithTasks,
    TeamMember,
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
    | { kind: "teamMember"; teamMember: TeamMember }
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
    | { kind: "teamMember"; teamMember: TeamMember }
    | { kind: "unassigned" };

export interface TasksPerUser {
    unassigned: number;
    assigned: Map<string, number>;
}

export type DestructiveOverlayType =
    | { kind: "deleteLabel"; label: Label }
    | { kind: "deleteTeamMember"; teamMember: TeamMember }
    | {
          kind: "deleteSection";
          section: Section;
      }
    | { kind: "deleteTask"; task: Task }
    // XXX this is never used
    | { kind: "deleteSelectedTasks"; tasks: Task[] }
    | { kind: "archiveProject"; project: Project }
    | { kind: "deleteProject"; project: Project };

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
    | {
          kind: "project";
          workspace: Workspace;
          project: Project;
      }
    | {
          kind: "section";
          project: Project;
          section: Section;
      }
    | {
          kind: "task";
          task: TaskWithSection;
          location: "task";
          // TODO remove this property
          section: Section;
      }
    | {
          kind: "task";
          task: TaskWithSection;
          location: "dashboard";
          // TODO remove this property?
          section: SectionWithTasks;
          project: ProjectDetail;
      }
    | { kind: "help" }
    | { kind: "permissions" }
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
    | { kind: "updateProject"; project: Project }
    | { kind: "createProject"; workspace: Workspace }
    | { kind: "inviteTeamMember"; workspace: Workspace }
    | { kind: "createSection"; project: Project }
    | {
          kind: "updateSection";
          section: Section;
      }
    | { kind: "recoverProject"; project: Project };
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
    | { kind: "saving" };

// TODO rename FormViewState
export type FormViewState =
    | { kind: "start" }
    | { kind: "submitting" }
    | { kind: "error"; message: string };
