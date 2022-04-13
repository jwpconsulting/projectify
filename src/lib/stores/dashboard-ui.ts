import { writable } from "svelte/store";
export const dashboardSectionsLayout = writable<"grid" | "list">("list");
