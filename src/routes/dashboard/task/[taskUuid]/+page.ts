import { currentTaskUuid } from "$lib/stores/dashboard";

export const prerender = false;
export const ssr = false;

export function load({
    params: { taskUuid },
}: {
    params: { taskUuid: string };
}) {
    currentTaskUuid.set(taskUuid);
}
