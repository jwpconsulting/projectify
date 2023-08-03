import type { LayoutLoadEvent } from "./$types";

import { currentWorkspaceUuid } from "$lib/stores/dashboard";

export const ssr = false;
export const prerender = false;

export function load({ params: { workspaceUuid } }: LayoutLoadEvent) {
    currentWorkspaceUuid.set(workspaceUuid);
}
