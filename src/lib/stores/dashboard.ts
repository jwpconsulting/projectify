import {
    Mutation_MoveTaskAfter,
    Mutation_DeleteTask,
    Mutation_AssignTask,
} from "./../graphql/operations";
import { goto } from "$app/navigation";
import Fuse from "fuse.js";
import lodash from "lodash";
import { writable } from "svelte/store";
import { client } from "$lib/graphql/client";
import { getModal } from "$lib/components/dialogModal.svelte";
import type {
    Label,
    Task,
    WorkspaceBoardSection,
    Workspace,
    WorkspaceUser,
} from "$lib/types";
import { getDashboardWorkspaceBoardUrl, getDashboardTaskUrl } from "$lib/urls";

export const drawerModalOpen = writable(false);
export const currentWorkspace = writable<Workspace | null>(null);
export const currentBoardUuid = writable<string | null>(null);
export const currentTaskDetailsUuid = writable<string | null>(null);
export const newTaskSectionUuid = writable<string | null>(null);
export const currentBoardSections = writable<WorkspaceBoardSection[]>([]);
export const loading = writable<boolean>(false);

export const fuseSearchThreshold = 0.3;

export function openNewTask(sectionUuid: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUuid.set(sectionUuid);
    currentTaskDetailsUuid.set(null);
}
export function openTaskDetails(
    workspaceBoardUuid: string,
    taskUuid: string,
    _subView: string | null = null
): void {
    drawerModalOpen.set(true);
    currentTaskDetailsUuid.set(taskUuid);
    goto(
        getDashboardTaskUrl(
            workspaceBoardUuid,
            taskUuid,
            _subView || "details"
        )
    );
}
export function closeTaskDetails(): void {
    drawerModalOpen.set(false);
    currentTaskDetailsUuid.set(null);

    // const workspaceUuid = get(currentWorkspace);
    // const boardUuid = get(currentBoardUuid);

    // XXX gotoDashboard(workspaceUuid, boardUuid, null);
}

export function gotoWorkspaceBoard(workspaceBoardUuid: string) {
    goto(getDashboardWorkspaceBoardUrl(workspaceBoardUuid));
}

export function copyDashboardURL(
    _workspaceUuid: string | null = null,
    _boardUuid: string | null = null,
    _taskUuid: string | null = null
): void {
    const path = "";
    const url = `${location.protocol}//${location.host}${path}`;
    navigator.clipboard.writeText(url);
}

export function pushTashUuidtoPath(_uuid: string): void {
    // const workspaceUuid = get(currentWorkspace).uuid;
    // const boardUuid = get(currentBoardUuid);
    // if (workspaceUuid && boardUuid) {
    // XXX gotoDashboard(workspaceUuid, boardUuid, uuid);
    // }
}

export const currentWorkspaceLabels = writable<Label[]>([]);

export function filterSectionsTasks(
    sections: WorkspaceBoardSection[],
    labels: Label[],
    assignee: WorkspaceUser | "unassigned" | null
): WorkspaceBoardSection[] {
    if (labels.length) {
        const labelUuids = new Map<string, boolean>();

        labels.forEach((l) => {
            labelUuids.set(l.uuid, true);
        });

        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.get(l.uuid) ? true : false
                    ) >= 0
                );
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    if (assignee) {
        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                if (assignee === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee?.user.email === assignee.user.email;
                }
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    return sections;
}

export function searchTasks(
    sections: WorkspaceBoardSection[],
    searchText: string
): Task[] {
    const tasks: Task[] = lodash.flatten(
        sections.map((section) => (section.tasks ? section.tasks : []))
    );

    const searchEngine: Fuse<Task> = new Fuse(tasks, {
        keys: ["title"],
        threshold: fuseSearchThreshold,
    });

    return searchEngine
        .search(searchText)
        .map((res: Fuse.FuseResult<Task>) => res.item);
}

export async function moveTaskAfter(
    taskUuid: string,
    workspaceBoardSectionUuid: string,
    afterTaskUuid: string | null = null
): Promise<void> {
    try {
        const input: {
            taskUuid: string;
            workspaceBoardSectionUuid: string;
            afterTaskUuid?: string;
        } = {
            taskUuid,
            workspaceBoardSectionUuid,
        };

        if (afterTaskUuid) {
            input.afterTaskUuid = afterTaskUuid;
        }

        await client.mutate({
            mutation: Mutation_MoveTaskAfter,
            variables: { input },
        });
    } catch (error) {
        console.error(error);
    }
}

export async function deleteTask(task: Task): Promise<void> {
    const modalRes = await getModal("deleteTaskConfirmModal").open();

    if (!modalRes) {
        return;
    }

    try {
        await client.mutate({
            mutation: Mutation_DeleteTask,
            variables: {
                input: {
                    uuid: task.uuid,
                },
            },
        });

        closeTaskDetails();
    } catch (error) {
        console.error(error);
    }
}

export async function assignUserToTask(
    userEmail: string | null,
    taskUuid: string
): Promise<void> {
    try {
        await client.mutate({
            mutation: Mutation_AssignTask,
            variables: {
                input: {
                    uuid: taskUuid,
                    email: userEmail,
                },
            },
        });
    } catch (error) {
        console.error(error);
    }
}
