import Sarus from "@anephenix/sarus";
import type { Unsubscriber, Subscriber, Readable } from "svelte/store";
import { writable } from "svelte/store";

import { browser } from "$app/environment";

interface Message {
    type: string;
    uuid: string;
    data: unknown;
}

export interface WsMessage {
    message: Message;
    timeStamp: number;
}

// A svelte store subscriber that received WSMessages
type WsSubscriber = Subscriber<WsMessage>;

const wsSubscriptionStores = new Map<string, WsSubscriptionStore>();

export type WsSubscriptionStore = Readable<WsMessage>;

function makeWsSubscriptionStore(url: string): WsSubscriptionStore {
    const subscribers = new Set<WsSubscriber>();

    const onMessage = (event: MessageEvent<string>) => {
        const message: Message = JSON.parse(event.data) as Message;
        const { timeStamp } = event;
        subscribers.forEach((run) => run({ message, timeStamp }));
    };

    const sarus = new Sarus({
        url,
        eventListeners: {
            open: [console.debug.bind(null, "Connection opened to", url)],
            close: [console.debug.bind(null, "Connection closed to", url)],
            error: [console.error.bind(null, "Connection error for", url)],
            message: [onMessage],
        },
    });

    const unsubscribe = (run: WsSubscriber): void => {
        subscribers.delete(run);
        if (subscribers.size > 0) {
            return;
        }
        sarus.disconnect();
        wsSubscriptionStores.delete(url);
        console.debug("Cleaned up store for", url);
    };
    const subscribe = (run: WsSubscriber): Unsubscriber => {
        subscribers.add(run);
        return () => unsubscribe(run);
    };
    return {
        subscribe,
    };
}

export function getSubscriptionFor(url: string): WsSubscriptionStore {
    const store = wsSubscriptionStores.get(url);
    if (store) {
        return store;
    }
    const newStore: WsSubscriptionStore = makeWsSubscriptionStore(url);
    wsSubscriptionStores.set(url, newStore);
    return newStore;
}
// Online connection

export const online = writable(true);

if (browser) {
    setTimeout(() => {
        online.set(navigator.onLine);
    }, 1000);

    window.addEventListener("offline", () => {
        online.set(false);
    });

    window.addEventListener("online", () => {
        online.set(true);
    });
}
