import type { Subscriber } from "svelte/store";

type WSStore = { message: string; at: number };
type WSSubscriber = Subscriber<WSStore>;

export class WSSubscriptionStore {
    public store: WSStore;
    subscribers = [];
    socket: WebSocket;

    constructor(public url: string) {
        this.socket = new WebSocket(url);

        this.socket.onmessage = ({ data, timeStamp }) => {
            this.store = {
                message: data,
                at: timeStamp,
            };
            this.dispatch();
        };
    }

    dispatch(): void {
        for (let i = 0; i < this.subscribers.length; i += 1) {
            this.subscribers[i](this.store);
        }
    }

    public subscribe(subscriber: WSSubscriber): () => void {
        this.subscribers.push(subscriber);

        subscriber(this.store);

        return () => {
            const index = this.subscribers.indexOf(subscriber);
            if (index !== -1) {
                this.subscribers.splice(index, 1);
            }
            if (!this.subscribers.length) {
                this.socket.close();
                stores[this.url] = null;
                delete stores[this.url];
            }
        };
    }
}

type WSSubscriptionStoreMap = {
    [key: string]: WSSubscriptionStore;
};

const stores: WSSubscriptionStoreMap = {};

export function getSubscriptionFor(url: string): WSSubscriptionStore {
    if (!stores[url]) {
        stores[url] = new WSSubscriptionStore(url);
    }
    return stores[url];
}
