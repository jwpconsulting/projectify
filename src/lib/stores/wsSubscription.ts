import delay from "delay";
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

const retryTimeStart = 2000;
const retryTimeMult = 1.1;
const retryTimeJitter = 500;
const maxRetryTime = 20000;

export class WSSubscriptionStore {
    wsMessage: WSMessage | null = null;
    subscribers: WSSubscriber[] = [];
    socket: WebSocket;
    socketActive = true;
    url: string;

    retryingConnection = false;

    retryTime: number;

    constructor(url: string) {
        this.url = url;
        this.retryTime = retryTimeStart;
        this.socket = this.createNewConnection();
        startWatchDog();
        this.debug("constructor");
    }

    deleteConnection(): void {
        this.socket.onmessage = null;
        this.socket.onclose = null;
        this.socket.onerror = null;
        this.socket.close();
        this.socketActive = false;
    }

    createNewConnection(): WebSocket {
        this.debug("Creating new connection");
        const socket = new WebSocket(this.url);
        socket.onmessage = ({
            data,
            timeStamp,
        }: {
            data: string;
            timeStamp: number;
        }) => {
            this.debug("socket.onmessage", data, timeStamp);
            this.wsMessage = {
                message: data,
                at: timeStamp,
            };
            this.dispatch();
        };
        socket.onopen = (event) => {
            this.debug("socket.onopen", event);
            this.retryTime = retryTimeStart;
            this.retryingConnection = false;
            // this.dispatch();
        };
        socket.onclose = async (event) => {
            this.debug("socket.onclose", event);
            await this.retryConnection();
        };
        socket.onerror = async (event) => {
            this.debug("socket.onerror", event);
            await this.retryConnection();
        };
        return socket;
    }

    recreateConnection() {
        this.debug("Recreating connection");
        this.deleteConnection();
        this.createNewConnection();
    }

    async retryConnection(now = false) {
        this.debug("Retrying connection", { now });
        if (this.retryingConnection) {
            this.debug("Already retrying connection");
            return;
        }

        this.retryingConnection = true;

        const delayTime = this.retryTime + Math.random() * retryTimeJitter;

        this.retryTime *= retryTimeMult;
        this.retryTime = Math.min(this.retryTime, maxRetryTime);

        if (now) {
            this.retryTime = 0;
        } else {
            await delay(delayTime);
        }

        if (this.socket.readyState == WebSocket.CLOSED) {
            this.recreateConnection();
        }
    }

    dispatch() {
        this.debug("Dispatching", this.wsMessage, this.subscribers);
        this.subscribers.forEach((subscriber) => {
            subscriber(this.wsMessage);
        });
    }

    public subscribe(subscriber: WSSubscriber): () => Promise<void> {
        this.subscribers.push(subscriber);
        this.debug("Pushing", subscriber);

        return async () => {
            const index = this.subscribers.indexOf(subscriber);
            if (index !== -1) {
                this.subscribers.splice(index, 1);
            }
            if (!this.subscribers.length) {
                this.deleteConnection();
                wsSubscriptionStores.delete(this.url);
                await stopWatchDog();
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

let watchDogTimer: number | null = null;
let watchDogLastTime = 0;
const watchDogInterval = 1000;

function startWatchDog(): void {
    if (!browser) {
        return;
    }
    if (watchDogTimer) {
        console.log("Watchdog timer already created");
        return;
    }
    if (watchDogLastTime == 0) {
        watchDogLastTime = Date.now();
    }
    if (watchDogTimer) {
        window.clearInterval(watchDogTimer);
    }
    watchDogTimer = window.setInterval(async () => {
        const now = Date.now();
        watchDogLastTime = now;

        await checkAllConnectionStatus();
    }, watchDogInterval);
}

async function stopWatchDog(): Promise<void> {
    if (!watchDogTimer) {
        throw new Error("Expected watchDogTimer");
    }
    const connectionActive = wsSubscriptionStores.size > 0;
    if (!connectionActive) {
        window.clearInterval(watchDogTimer);
    }
    await checkAllConnectionStatus();
}

async function checkAllConnectionStatus() {
    const activeWSS = wsSubscriptionStores.size;
    let activeCon = 0;

    wsSubscriptionStores.forEach((wsSubscriptionStore) => {
        const { socketActive } = wsSubscriptionStore;
        const { readyState } = wsSubscriptionStore.socket;
        const openOrConnecting =
            readyState == WebSocket.OPEN || readyState == WebSocket.CONNECTING;
        if (socketActive && openOrConnecting) {
            activeCon++;
        } else {
            console.log({ wsSubscriptionStore, socketActive, readyState });
        }
    });

    activeWSSubscriptions.set(activeWSS);
    activeWSConnections.set(activeCon);

    if (activeWSS === activeCon) {
        return;
    }
    console.log("Retrying all connections");
    const promises = [...wsSubscriptionStores.values()].map(
        (wsSubscriptionStore) => {
            return wsSubscriptionStore.retryConnection(true);
        }
    );
    await Promise.all(promises);
    // XXX
    // This enters an infite loop here
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
