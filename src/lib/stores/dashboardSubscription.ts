import vars from "$lib/env";
import {
    getSubscriptionFor,
    WSSubscriptionStore,
} from "$lib/stores/wsSubscription";

export const getSubscriptionForCollection = (
    collection: "workspace" | "workspace-board" | "task",
    uuid: string
): WSSubscriptionStore | null => {
    let wsEndPoint = vars.WS_ENDPOINT;
    if (wsEndPoint.indexOf("/ws") == 0) {
        wsEndPoint = `ws://${location.host}${wsEndPoint}`;
    }
    const wsURL = `${wsEndPoint}/${collection}/${uuid}/`;

    return getSubscriptionFor(wsURL);
};
