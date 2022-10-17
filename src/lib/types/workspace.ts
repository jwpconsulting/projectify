import type { TimestampedType, TitleDescriptionType } from "$lib/types/base";
import type { User } from "$lib/types/user";
import type { WorkspaceBoardSection } from "$lib/types";

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

export type ChatMessage = {
    author: WorkspaceUser;
    uuid: string;
    text: string;
} & TimestampedType;

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
