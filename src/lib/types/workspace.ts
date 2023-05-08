import type { TimestampedType, TitleDescriptionType } from "$lib/types/base";
import type { User } from "$lib/types/user";

export type WorkspaceUser = {
    user: User;
    uuid: string;
    job_title?: string;
    role: string;
} & TimestampedType;

export type Label = {
    name: string;
    color: number;
    uuid: string;
};

export type SubTask = {
    uuid: string;
    done: boolean;
    order: number;
} & TimestampedType &
    TitleDescriptionType;

export type NewSubTask = {
    task: Task;
};

export type CreateSubTask = TitleDescriptionType;

export type ChatMessage = {
    author: WorkspaceUser;
    uuid: string;
    text: string;
} & TimestampedType;

// What is needed to know at least to create a new task
export type NewTask = {
    workspace_board_section: WorkspaceBoardSection;
};

// What is submitted to the API to create the actual task
// TODO
export type CreateTask = TitleDescriptionType &
    NewTask & {
        // XXX for some reason our API thinks this one is a required field
        description: string;
        labels: Label[];
        assignee?: WorkspaceUser;
        sub_tasks?: SubTask[];
        // There is a mismatch for this in the backend and frontend
        // Normally, we should be accepting undefined here as well?
        // I get this error
        // Uncaught (in promise) ApolloError: AddTaskInput.__init__() missing 1 required positional argument: 'deadline'
        deadline: string | null;
    };

// All the info we can receive from the API
export type Task = {
    _order: number;
    uuid: string;
    deadline?: string;
    number: number;
    labels: Label[];
    assignee?: WorkspaceUser;
    workspace_board_section?: WorkspaceBoardSection;
    sub_tasks?: SubTask[];
    chat_messages?: ChatMessage[];
} & TimestampedType &
    TitleDescriptionType;

export type CreateWorkspaceBoardSection = TitleDescriptionType;

export type WorkspaceBoardSection = {
    _order: number;
    uuid: string;
    tasks?: Task[];
    workspace_board?: WorkspaceBoard;
} & TimestampedType &
    CreateWorkspaceBoardSection;

export type WorkspaceBoard = {
    deadline?: string;
    uuid: string;
    workspace_board_sections?: WorkspaceBoardSection[];
    archived?: string;
    workspace?: Workspace;
} & TimestampedType &
    TitleDescriptionType;

export type Workspace = {
    picture?: string;
    workspace_users?: WorkspaceUser[];
    workspace_boards?: WorkspaceBoard[];
    labels?: Label[];
    uuid: string;
} & TimestampedType &
    TitleDescriptionType;
