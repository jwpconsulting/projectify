import vars from "$lib/env";
import {
    getSubscriptionFor,
    WSSubscriptionStore,
} from "$lib/stores/wsSubscription";

export const getSubscriptionForCollection = (
    collection: "workspace" | "workspace-board" | "task",
    uuid: string
): WSSubscriptionStore => {
    let wsEndPoint = vars.WS_ENDPOINT;
    if (wsEndPoint.indexOf("ws://") == -1) {
        wsEndPoint = `ws://${location.host}${wsEndPoint}`;
    }
    const wsURL = `${vars.WS_ENDPOINT}/${collection}/${uuid}/`;
    return getSubscriptionFor(wsURL);
};
