import {
    Mutation_MoveTaskAfter,
    Mutation_DeleteTask,
    Mutation_AssignTask,
} from "./../graphql/operations";
import { goto } from "$app/navigation";
import Fuse from "fuse.js";
import lodash from "lodash";
import { writable, derived } from "svelte/store";
import { client } from "$lib/graphql/client";
import { getModal } from "$lib/components/dialogModal.svelte";
import type {
    Customer,
    Label,
    Task,
    WorkspaceBoardSection,
    Workspace,
    WorkspaceUser,
    WorkspaceBoard,
    LabelSelection,
    LabelSelectionInput,
    WorkspaceUserSelectionInput,
    WorkspaceUserSelection,
} from "$lib/types";
import { getDashboardWorkspaceBoardUrl, getDashboardTaskUrl } from "$lib/urls";
import { get } from "svelte/store";
import {
    getTask,
    getWorkspace,
    getWorkspaces,
    getWorkspaceBoard,
    getWorkspaceCustomer,
    getArchivedWorkspaceBoards,
} from "$lib/repository";
import { browser } from "$app/env";
import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

export const drawerModalOpen = writable(false);
export const currentWorkspaceUuid = writable<string | null>(null);
export const currentWorkspaceBoardUuid = writable<string | null>(null);
export const currentTaskUuid = writable<string | null>(null);
export const newTaskSectionUuid = writable<string | null>(null);
export const loading = writable<boolean>(false);

let currentWorkspaceSubscription: WSSubscriptionStore | null = null;
let currentWorkspaceSubscriptionUnsubscribe: (() => void) | null = null;
let currentWorkspaceBoardSubscription: WSSubscriptionStore | null = null;
let currentWorkspaceBoardSubscriptionUnsubscribe: (() => void) | null = null;
let currentTaskSubscription: WSSubscriptionStore | null = null;
let currentTaskSubscriptionUnsubscribe: (() => void) | null = null;

export const currentWorkspace = derived<
    [typeof currentWorkspaceUuid],
    Workspace | null
>(
    [currentWorkspaceUuid],
    ([$currentWorkspaceUuid], set) => {
        if (!browser) {
            set(null);
            return;
        }
        if (!$currentWorkspaceUuid) {
            set(null);
            return;
        }
        set(null);
        getWorkspace($currentWorkspaceUuid).then((workspace) =>
            set(workspace)
        );
        if (currentWorkspaceSubscriptionUnsubscribe) {
            currentWorkspaceSubscriptionUnsubscribe();
        }
        currentWorkspaceSubscription = getSubscriptionForCollection(
            "workspace",
            $currentWorkspaceUuid
        );
        if (!currentWorkspaceSubscription) {
            throw new Error("Expected currentWorkspaceSubscription");
        }
        currentWorkspaceSubscriptionUnsubscribe =
            currentWorkspaceSubscription.subscribe(async (_value) => {
                console.log("Refetching workspace", $currentWorkspaceUuid);
                set(await getWorkspace($currentWorkspaceUuid));
            });
    },
    null
);
export const currentArchivedWorkspaceBoards = derived<
    [typeof currentWorkspace],
    WorkspaceBoard[]
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        set([]);
        if (!$currentWorkspace) {
            return;
        }
        getArchivedWorkspaceBoards($currentWorkspace.uuid).then(
            (archivedWorkspaceBoards) => set(archivedWorkspaceBoards)
        );
    },
    []
);

export const currentWorkspaceBoard = derived<
    [typeof currentWorkspaceBoardUuid],
    WorkspaceBoard | null
>([currentWorkspaceBoardUuid], ([$currentWorkspaceBoardUuid], set) => {
    if (!browser) {
        set(null);
        return;
    }
    if (!$currentWorkspaceBoardUuid) {
        set(null);
        return;
    }
    set(null);
    getWorkspaceBoard($currentWorkspaceBoardUuid).then((workspaceBoard) =>
        set(workspaceBoard)
    );
    if (currentWorkspaceBoardSubscriptionUnsubscribe) {
        currentWorkspaceBoardSubscriptionUnsubscribe();
    }
    currentWorkspaceBoardSubscription = getSubscriptionForCollection(
        "workspace-board",
        $currentWorkspaceBoardUuid
    );
    if (!currentWorkspaceBoardSubscription) {
        throw new Error("Expected currentWorkspaceBoardSubscription");
    }
    currentWorkspaceBoardSubscriptionUnsubscribe =
        currentWorkspaceBoardSubscription.subscribe(async (_value) => {
            console.log(
                "Refetching workspaceBoard",
                $currentWorkspaceBoardUuid
            );
            set(await getWorkspaceBoard($currentWorkspaceBoardUuid));
        });
});
const ensureWorkspaceUuid = derived<
    [typeof currentWorkspaceUuid, typeof currentWorkspaceBoard],
    string | null
>(
    [currentWorkspaceUuid, currentWorkspaceBoard],
    ([$currentWorkspaceUuid, $currentWorkspaceBoard], set) => {
        // $currentWorkspaceUuid has already been set
        if ($currentWorkspaceUuid) {
            return;
        }
        if (!$currentWorkspaceBoard) {
            return;
        }
        if (!$currentWorkspaceBoard.workspace) {
            console.error("Expected $currentWorkspaceBoard.workspace");
            return;
        }
        set($currentWorkspaceBoard.workspace.uuid);
    },
    null
);
ensureWorkspaceUuid.subscribe((workspaceUuid: string | null) => {
    if (!workspaceUuid) {
        return;
    }
    currentWorkspaceUuid.set(workspaceUuid);
});

export const currentCustomer = derived<
    [typeof currentWorkspace],
    Customer | null
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        if (!$currentWorkspace) {
            set(null);
            return;
        }
        set(null);
        getWorkspaceCustomer($currentWorkspace.uuid).then((customer) =>
            set(customer)
        );
    },
    null
);

export const currentTask = derived<[typeof currentTaskUuid], Task | null>(
    [currentTaskUuid],
    ([$currentTaskUuid], set) => {
        if (!browser) {
            set(null);
            return;
        }
        if (!$currentTaskUuid) {
            set(null);
            return;
        }
        set(null);
        getTask($currentTaskUuid).then((task) => set(task));
        if (currentTaskSubscriptionUnsubscribe) {
            currentTaskSubscriptionUnsubscribe();
        }
        currentTaskSubscription = getSubscriptionForCollection(
            "task",
            $currentTaskUuid
        );
        if (!currentTaskSubscription) {
            throw new Error("Expected currentWorkspaceBoardSubscription");
        }
        currentTaskSubscriptionUnsubscribe = currentTaskSubscription.subscribe(
            async (_value) => {
                console.log("Refetching task", $currentTaskUuid);
                set(await getTask($currentTaskUuid));
            }
        );
    },
    null
);

export const fuseSearchThreshold = 0.3;

export function openNewTask(sectionUuid: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUuid.set(sectionUuid);
    currentTaskUuid.set(null);
}
export function openTaskDetails(
    workspaceBoardUuid: string,
    taskUuid: string,
    subView: string = "details"
) {
    drawerModalOpen.set(true);
    currentTaskUuid.set(taskUuid);
    goto(getDashboardTaskUrl(workspaceBoardUuid, taskUuid, subView));
}
export function closeTaskDetails(): void {
    drawerModalOpen.set(false);
    currentTaskUuid.set(null);
    const boardUuid = get(currentWorkspaceBoardUuid);
    if (!boardUuid) {
        throw new Error("Expected boardUuid");
    }
    goto(getDashboardWorkspaceBoardUrl(boardUuid));
}

export function copyDashboardURL(
    workspaceBoardUuid: string,
    taskUuid: string | null = null
): void {
    const path = taskUuid
        ? getDashboardTaskUrl(workspaceBoardUuid, taskUuid, "details")
        : getDashboardWorkspaceBoardUrl(workspaceBoardUuid);
    const url = `${location.protocol}//${location.host}${path}`;
    navigator.clipboard.writeText(url);
}

export function pushTashUuidtoPath() {
    const boardUuid = get(currentWorkspaceBoardUuid);
    if (!boardUuid) {
        throw new Error("Expected boardUuid");
    }
    goto(getDashboardWorkspaceBoardUrl(boardUuid));
}

export const currentWorkspaceLabels = derived<
    [typeof currentWorkspace],
    Label[]
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        if (!$currentWorkspace) {
            set([]);
            return;
        }
        if (!$currentWorkspace.labels) {
            throw new Error("Expected $currentWorkspace.labels");
        }
        set($currentWorkspace.labels);
    },
    []
);

export const currentWorkspaceUsers = derived<
    [typeof currentWorkspace],
    WorkspaceUser[]
>(
    [currentWorkspace],
    ([$currentWorkspace], set) => {
        if (!$currentWorkspace) {
            set([]);
            return;
        }
        if (!$currentWorkspace.workspace_users) {
            throw new Error("Expected $currentWorkspace.workspace_users");
        }
        set($currentWorkspace.workspace_users);
    },
    []
);

export const labelSearch = writable<string>("");
export const workspaceUserSearch = writable<string>("");

function searchLabels(labels: Label[], searchInput: string): Label[] {
    if (searchInput === "") {
        return labels;
    }
    const searchEngine = new Fuse(labels, {
        keys: ["name"],
        threshold: fuseSearchThreshold,
        shouldSort: false,
    });
    const result = searchEngine.search(searchInput);
    return result.map((res: Fuse.FuseResult<Label>) => res.item);
}

export const labelSearchResults = derived<
    [typeof currentWorkspaceLabels, typeof labelSearch],
    Label[]
>(
    [currentWorkspaceLabels, labelSearch],
    ([$currentWorkspaceLabels, $labelSearch], set) => {
        set(searchLabels($currentWorkspaceLabels, $labelSearch));
    },
    []
);

function searchWorkspaceUsers(
    workspaceUsers: WorkspaceUser[],
    searchInput: string
) {
    if (searchInput === "") {
        return workspaceUsers;
    }
    const searchEngine = new Fuse(workspaceUsers, {
        keys: ["user.email", "user.full_name"],
        threshold: fuseSearchThreshold,
        shouldSort: false,
    });
    const result = searchEngine.search(searchInput);
    return result.map((res: Fuse.FuseResult<WorkspaceUser>) => res.item);
}

export const workspaceUserSearchResults = derived<
    [typeof currentWorkspaceUsers, typeof workspaceUserSearch],
    WorkspaceUser[]
>(
    [currentWorkspaceUsers, workspaceUserSearch],
    ([$currentWorkspaceUsers, $workspaceUserSearch], set) => {
        set(
            searchWorkspaceUsers($currentWorkspaceUsers, $workspaceUserSearch)
        );
    },
    []
);

export const selectedLabels = writable<LabelSelection>({ kind: "allLabels" });
export const selectedWorkspaceUser = writable<WorkspaceUserSelection>({
    kind: "allWorkspaceUsers",
});

export function selectWorkspaceUser(selection: WorkspaceUserSelectionInput) {
    selectedWorkspaceUser.update(
        (currentSelection: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if (currentSelection.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if (currentSelection.kind === "workspaceUsers") {
                    currentSelection.workspaceUserUuids.add(selectionUuid);
                    return currentSelection;
                } else {
                    const workspaceUserUuids = new Set<string>();
                    workspaceUserUuids.add(selectionUuid);
                    return { kind: "workspaceUsers", workspaceUserUuids };
                }
            }
        }
    );
}

export function deselectWorkspaceUser(selection: WorkspaceUserSelectionInput) {
    selectedWorkspaceUser.update(
        (currentSelection: WorkspaceUserSelection) => {
            if (selection.kind === "allWorkspaceUsers") {
                return { kind: "allWorkspaceUsers" };
            } else if (selection.kind === "unassigned") {
                if (currentSelection.kind === "unassigned") {
                    return { kind: "allWorkspaceUsers" };
                } else {
                    return { kind: "unassigned" };
                }
            } else {
                const selectionUuid = selection.workspaceUser.uuid;
                if (currentSelection.kind === "workspaceUsers") {
                    currentSelection.workspaceUserUuids.delete(selectionUuid);
                    if (currentSelection.workspaceUserUuids.size === 0) {
                        return { kind: "allWorkspaceUsers" };
                    } else {
                        return currentSelection;
                    }
                } else {
                    return { kind: "allWorkspaceUsers" };
                }
            }
        }
    );
}
export function selectLabel(selection: LabelSelectionInput) {
    selectedLabels.update((selectedLabels) => {
        if (selection.kind == "label") {
            if (selectedLabels.kind === "labels") {
                if (selectedLabels.labelUuids.has(selection.labelUuid)) {
                    selectedLabels.labelUuids.delete(selection.labelUuid);
                    if (selectedLabels.labelUuids.size === 0) {
                        return { kind: "allLabels" };
                    }
                } else {
                    selectedLabels.labelUuids.add(selection.labelUuid);
                }
                return selectedLabels;
            } else {
                return {
                    kind: "labels",
                    labelUuids: new Set([selection.labelUuid]),
                };
            }
        } else if (selection.kind == "noLabel") {
            if (selectedLabels.kind === "noLabel") {
                return { kind: "allLabels" };
            } else {
                return { kind: "noLabel" };
            }
        } else {
            return { kind: "allLabels" };
        }
    });
}

type CurrentFilter = {
    labels: LabelSelection;
    workspaceUser: WorkspaceUserSelection;
    workspaceBoardSections: WorkspaceBoardSection[];
};
export const currentWorkspaceBoardSections = derived<
    [
        typeof selectedLabels,
        typeof selectedWorkspaceUser,
        typeof currentWorkspaceBoard
    ],
    WorkspaceBoardSection[]
>(
    [selectedLabels, selectedWorkspaceUser, currentWorkspaceBoard],
    (
        [$selectedLabels, $selectedWorkspaceUser, $currentWorkspaceBoard],
        set
    ) => {
        if (!$currentWorkspaceBoard) {
            return;
        }
        const workspaceBoardSections =
            $currentWorkspaceBoard.workspace_board_sections;
        if (!workspaceBoardSections) {
            return;
        }
        set(
            filterSectionsTasks({
                labels: $selectedLabels,
                workspaceUser: $selectedWorkspaceUser,
                workspaceBoardSections,
            })
        );
    },
    []
);

type TasksPerUser = { unassigned: number; assigned: Map<string, number> };
export const tasksPerUser = derived<
    [typeof currentWorkspaceBoardSections],
    TasksPerUser
>(
    [currentWorkspaceBoardSections],
    ([$currentWorkspaceBoardSections], set) => {
        const userCounts = new Map<string, number>();
        let unassignedCounts = 0;
        $currentWorkspaceBoardSections.forEach((section) => {
            if (!section.tasks) {
                return;
            }
            section.tasks.forEach((task) => {
                if (task.assignee) {
                    const uuid = task.assignee.uuid;
                    const count = userCounts.get(uuid);
                    if (count) {
                        userCounts.set(uuid, count + 1);
                    } else {
                        userCounts.set(uuid, 1);
                    }
                } else {
                    unassignedCounts = unassignedCounts + 1;
                }
            });
        });
        const counts: TasksPerUser = {
            unassigned: unassignedCounts,
            assigned: userCounts,
        };
        console.log(counts);
        set(counts);
    },
    { unassigned: 0, assigned: new Map<string, number>() }
);

export function filterSectionsTasks(
    currentFilter: CurrentFilter
): WorkspaceBoardSection[] {
    let sections: WorkspaceBoardSection[] =
        currentFilter.workspaceBoardSections;
    if (currentFilter.labels.kind === "noLabel") {
    } else if (currentFilter.labels.kind === "allLabels") {
    } else {
        const labelUuids = [...currentFilter.labels.labelUuids.keys()];

        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.find((labelUuid) => l.uuid === labelUuid)
                            ? true
                            : false
                    ) >= 0
                );
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    const workspaceUserSelection = currentFilter.workspaceUser;
    if (workspaceUserSelection.kind !== "allWorkspaceUsers") {
        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                if (workspaceUserSelection.kind === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee
                        ? workspaceUserSelection.workspaceUserUuids.has(
                              task.assignee.uuid
                          )
                        : false;
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

export const taskSearchInput = writable<string>("");
// Clear on workspace board change
currentWorkspaceBoardUuid.subscribe((_uuid) => {
    selectedLabels.set({ kind: "allLabels" });
    selectedWorkspaceUser.set({ kind: "allWorkspaceUsers" });
    taskSearchInput.set("");
});
export const currentSearchedTasks = derived<
    [typeof currentWorkspaceBoardSections, typeof taskSearchInput],
    Task[] | null
>(
    [currentWorkspaceBoardSections, taskSearchInput],
    ([$currentWorkspaceBoardSections, $taskSearchInput], set) => {
        if ($taskSearchInput == "") {
            set(null);
        } else {
            set(searchTasks($currentWorkspaceBoardSections, $taskSearchInput));
        }
    },
    null
);

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

export async function setFirstWorkspace() {
    const workspaces = await getWorkspaces();
    let workspaceUuid;
    if (workspaces.length) {
        workspaceUuid = workspaces[0].uuid;
        currentWorkspaceUuid.set(workspaceUuid);
    } else {
        throw new Error("No workspaces");
    }
}

export async function setAndNavigateWorkspaceBoard(uuid: string) {
    currentWorkspaceBoardUuid.set(uuid);
    goto(getDashboardWorkspaceBoardUrl(uuid));
}

export const userExpandOpen = writable<boolean>(false);
export function toggleUserExpandOpen() {
    userExpandOpen.update((state) => !state);
}
export const labelExpandOpen = writable<boolean>(false);
export function toggleLabelExpandOpen() {
    labelExpandOpen.update((state) => !state);
}
