import Sarus from "@anephenix/sarus";
import type { Unsubscriber, Subscriber } from "svelte/store";
import { writable } from "svelte/store";
import { browser } from "$app/environment";

interface Message {
    type: string;
    uuid: string;
    data: unknown;
}

interface WSMessage {
    message: Message;
    at: number;
}

type WSSubscriber = Subscriber<WSMessage>;

const wsSubscriptionStores = new Map<string, WSSubscriptionStore>();

export interface WSSubscriptionStore {
    sarus: Sarus;
    subscribe: (run: WSSubscriber) => Unsubscriber;
    url: string;
}

function makeWsSubscriptionStore(url: string): WSSubscriptionStore {
    const subscribers = new Map<number, WSSubscriber>();
    let nextSubscriberId = 0;

    const message = ({ data, timeStamp: at }: MessageEvent<string>) => {
        const message: Message = JSON.parse(data) as Message;
        subscribers.forEach((subscriber) => subscriber({ message, at }));
    };

    const sarus = new Sarus({
        url,
        eventListeners: {
            open: [console.log.bind(null, "Connection opened to", url)],
            close: [console.log.bind(null, "Connection closed to", url)],
            error: [console.error.bind(null, "Connection error for", url)],
            message: [message],
        },
    });

    const unsubscribe = (id: number): void => {
        subscribers.delete(id);
        if (subscribers.size === 0) {
            sarus.disconnect();
            wsSubscriptionStores.delete(url);
        }
    };
    const subscribe = (run: WSSubscriber): Unsubscriber => {
        const subscriberId = nextSubscriberId;
        subscribers.set(subscriberId, run);
        nextSubscriberId++;
        return unsubscribe.bind(null, subscriberId, run);
    };
    return {
        sarus,
        url,
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
