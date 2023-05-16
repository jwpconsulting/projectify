import Sarus from "@anephenix/sarus";
import type { Subscriber } from "svelte/store";
import { writable } from "svelte/store";
import { browser } from "$app/environment";

interface WSMessage {
    message: string;
    at: number;
}
type WSSubscriber = Subscriber<WSMessage | null>;

const wsSubscriptionStores = new Map<string, WSSubscriptionStore>();

export const activeWSSubscriptions = writable(0);
export const activeWSConnections = writable(0);

export class WSSubscriptionStore {
    sarus: Sarus;
    subscribers: WSSubscriber[] = [];
    url: string;

    constructor(url: string) {
        this.url = url;
        this.sarus = new Sarus({ url });
        const onmessage = ({
            data,
            timeStamp,
        }: {
            data: string;
            timeStamp: number;
        }) => {
            this.debug("socket.onmessage", data, timeStamp);
            this.dispatch({
                message: data,
                at: timeStamp,
            });
        };
        this.sarus.on("message", onmessage);
    }

    dispatch(wsMessage: WSMessage) {
        this.debug("Dispatching", wsMessage, "to", this.subscribers);
        this.subscribers.forEach((subscriber) => {
            subscriber(wsMessage);
        });
    }

    public subscribe(subscriber: WSSubscriber): () => void {
        this.subscribers.push(subscriber);
        this.debug("Subscribing", subscriber);

        return () => {
            const index = this.subscribers.indexOf(subscriber);
            if (index !== -1) {
                this.subscribers.splice(index, 1);
            }
            if (!this.subscribers.length) {
                this.sarus.disconnect();
                wsSubscriptionStores.delete(this.url);
            }
        };
    }

    debug(reason: string, ...arg0: unknown[]) {
        console.debug(this.url, reason, { this: this }, ...arg0);
    }
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
    const newStore = new WSSubscriptionStore(url);
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
