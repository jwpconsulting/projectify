import type { SvelteComponent } from "svelte";
export type TabItem = {
    label: string;
    id: string;
    component?: typeof SvelteComponent;
    props?: unknown[];
    hidden?: boolean;
    url?: string;
};
