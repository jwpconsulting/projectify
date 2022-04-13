import { writable } from "svelte/store";
export const dashboardSectionsLayout = writable<"float" | "grid" | "list">(
    "list"
);
