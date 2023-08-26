import type { SvelteComponent } from "svelte";

export interface TabItem {
    label: string;
    id: string;
    component?: typeof SvelteComponent<object>;
    props?: unknown[];
    hidden?: boolean;
    url?: string;
}
