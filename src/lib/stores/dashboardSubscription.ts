import vars from "$lib/env";
import {
    getSubscriptionFor,
    WSSubscriptionStore,
} from "$lib/stores/wsSubscription";

export const getSubscriptionForCollection = (
    collection: "workspace-board" | "task",
    uuid: string
): WSSubscriptionStore => {
    const wsURL = `${vars.WS_ENDPOINT}/${collection}/${uuid}/`;
    return getSubscriptionFor(wsURL);
};
