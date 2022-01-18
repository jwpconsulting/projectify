import { writable } from "svelte/store";

export const drawerModalOpen = writable(false);
export const currenTaskDetailsUUID = writable<string | null>(null);

export function createNewTask(): void {
    drawerModalOpen.set(true);
    currenTaskDetailsUUID.set(null);
    console.log("createNewTask");
}
export function viewTaskDetails(taskUUID: string): void {
    drawerModalOpen.set(true);
    currenTaskDetailsUUID.set(taskUUID);
}
