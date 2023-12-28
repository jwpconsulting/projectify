import type { TimestampedType, TitleDescriptionType } from "$lib/types/base";
import type { User } from "$lib/types/user";

export type WorkspaceUser = {
    user: User;
    uuid: string;
    job_title?: string;
    role: string;
} & TimestampedType;

export interface Label {
    name: string;
    color: number;
    uuid: string;
}

export type SubTask = {
    uuid: string;
    done: boolean;
    order: number;
} & TimestampedType &
    TitleDescriptionType;

export type CreateUpdateSubTask = {
    done: boolean;
    // This will only exist for a sub task that is already inside a task
    uuid?: string;
} & TitleDescriptionType;

type ChatMessage = {
    author: WorkspaceUser;
    uuid: string;
    text: string;
} & TimestampedType;

// All the info we can receive from the API
export type Task = {
    _order: number;
    uuid: string;
    // TODO the following should be a Date
    deadline?: string;
    number: number;
    labels: Label[];
    assignee?: WorkspaceUser;
    workspace_board_section?: WorkspaceBoardSection;
    sub_tasks?: SubTask[];
    chat_messages?: ChatMessage[];
} & TimestampedType &
    TitleDescriptionType;

export type TaskWithWorkspaceBoardSection = Task & {
    workspace_board_section: WorkspaceBoardSection;
};

export type TaskWithWorkspace = Task & {
    workspace_board_section: WorkspaceBoardSection & {
        workspace_board: WorkspaceBoard & {
            workspace: Workspace;
        };
    };
};

export type CreateWorkspaceBoardSection = TitleDescriptionType;

export type WorkspaceBoardSection = {
    _order: number;
    uuid: string;
    tasks?: Task[];
    workspace_board?: WorkspaceBoard;
} & TimestampedType &
    CreateWorkspaceBoardSection;

export type WorkspaceBoardSectionWithTasks = WorkspaceBoardSection &
    Required<Pick<WorkspaceBoardSection, "tasks">>;

export type WorkspaceBoardSectionDetail = WorkspaceBoardSection &
    Required<Pick<WorkspaceBoardSection, "workspace_board" | "tasks">>;

export type WorkspaceBoard = {
    deadline?: string;
    uuid: string;
    workspace_board_sections?: WorkspaceBoardSection[];
    archived?: string;
    workspace?: Workspace;
} & TimestampedType &
    TitleDescriptionType;

export type WorkspaceBoardDetail = WorkspaceBoard & {
    workspace: Workspace;
    workspace_board_sections: WorkspaceBoardSectionWithTasks[];
};

export type ArchivedWorkspaceBoard = WorkspaceBoard & { archived: string };

export type Workspace = {
    picture: string | null;
    workspace_users?: WorkspaceUser[];
    workspace_boards?: WorkspaceBoard[];
    labels?: Label[];
    uuid: string;
} & TimestampedType &
    TitleDescriptionType;

export type WorkspaceDetail = Required<
    Pick<Workspace, "workspace_boards" | "labels" | "workspace_users">
> &
    Workspace;
