import Sarus from "@anephenix/sarus";
import type { Unsubscriber, Subscriber, Readable } from "svelte/store";
import { writable } from "svelte/store";

import { browser } from "$app/environment";

interface Message {
    type: string;
    uuid: string;
    data: unknown;
}

export interface WSMessage {
    message: Message;
    at: number;
}

// A svelte store subscriber that received WSMessages
type WSSubscriber = Subscriber<WSMessage>;

const wsSubscriptionStores = new Map<string, WSSubscriptionStore>();

export type WSSubscriptionStore = Readable<WSMessage>;

function makeWsSubscriptionStore(url: string): WSSubscriptionStore {
    const subscribers = new Set<WSSubscriber>();

    const message = ({ data, timeStamp: at }: MessageEvent<string>) => {
        const message: Message = JSON.parse(data) as Message;
        subscribers.forEach((subscriber) => subscriber({ message, at }));
    };

    const sarus = new Sarus({
        url,
        eventListeners: {
            open: [console.debug.bind(null, "Connection opened to", url)],
            close: [console.debug.bind(null, "Connection closed to", url)],
            error: [console.error.bind(null, "Connection error for", url)],
            message: [message],
        },
    });

    const unsubscribe = (run: WSSubscriber): void => {
        subscribers.delete(run);
        if (subscribers.size > 0) {
            return;
        }
        sarus.disconnect();
        wsSubscriptionStores.delete(url);
        console.debug("Cleaned up store for", url);
    };
    const subscribe = (run: WSSubscriber): Unsubscriber => {
        subscribers.add(run);
        return () => unsubscribe(run);
    };
    return {
        subscribe,
    };
}

export function getSubscriptionFor(url: string): WSSubscriptionStore | null {
    if (!browser) {
        console.debug("Expected browser");
        return null;
    }
    const store = wsSubscriptionStores.get(url);
    if (store) {
        return store;
    }
    const newStore: WSSubscriptionStore = makeWsSubscriptionStore(url);
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
