import type { TimestampedType } from "$lib/types/base";
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
