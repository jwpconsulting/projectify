import { writable } from "svelte/store";

export const drawerModalOpen = writable(false);
export const currenTaskDetailsUUID = writable<string | null>(null);
export const newTaskSectionUUID = writable<string | null>(null);

export function openNewTask(sectionUUID: string): void {
    drawerModalOpen.set(true);
    newTaskSectionUUID.set(sectionUUID);
    currenTaskDetailsUUID.set(null);
    console.log("createNewTask");
}
export function openTaskDetails(taskUUID: string): void {
    drawerModalOpen.set(true);
    currenTaskDetailsUUID.set(taskUUID);
}
export function closeTaskDetails(): void {
    drawerModalOpen.set(false);
}
