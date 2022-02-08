import { writable } from "svelte/store";
import vars from "$lib/env";
import type { ReadableQuery } from "svelte-apollo";
import debounce from "lodash/debounce.js";

let socket;

export const workspaceBoardSubscription = writable(null);

export function subscribeToWorkspaceBoard(
    uuid: string,
    queryToRefetch: ReadableQuery<any>
): void {
    console.log("subscribeToWorkspaceBoard", uuid);

    const wsURL = `${vars.WS_ENDPOINT}/workspace-board/${uuid}/`;

    if (socket) {
        socket.close();
    }
    socket = new WebSocket(wsURL);

    const refetch = debounce(({ data }) => {
        queryToRefetch.refetch();
        workspaceBoardSubscription.set(data);
    }, 100);

    socket.addEventListener("message", refetch);
}
