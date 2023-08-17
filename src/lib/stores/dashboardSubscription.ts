import vars from "$lib/env";

import { getSubscriptionFor } from "$lib/stores/wsSubscription";
import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";

export const getSubscriptionForCollection = (
    collection: "workspace" | "workspace-board" | "task",
    uuid: string
): WSSubscriptionStore | null => {
    let wsEndPoint = vars.WS_ENDPOINT;
    if (wsEndPoint.startsWith("/ws")) {
        wsEndPoint = `ws://${location.host}${wsEndPoint}`;
    }
    const wsURL = `${wsEndPoint}/${collection}/${uuid}/`;

    return getSubscriptionFor(wsURL);
};
