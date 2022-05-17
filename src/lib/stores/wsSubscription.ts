import { browser } from "$app/env";
import delay from "delay";
import type { Subscriber } from "svelte/store";
import { writable } from "svelte/store";

type WSStore = { message: string; at: number };
type WSSubscriber = Subscriber<WSStore>;

export const activeWSSubscriptions = writable(0);
export const activeWSConnections = writable(0);

export class WSSubscriptionStore {
    public store: WSStore;
    subscribers = [];
    socket: WebSocket = null;
    retryingConnection = false;

    public retryTimeStart = 2000;
    public retryTimeMult = 1.1;
    public retryTimeJitter = 500;
    public maxRetrieTime = 20000;

    retryTime: number;

    constructor(public url: string) {
        this.retryTime = this.retryTimeStart;
        this.createNewConnection();
        startWatchDog();
    }

    deleteConnection(): void {
        if (this.socket !== null) {
            this.socket.onmessage = null;
            this.socket.onclose = null;
            this.socket.onerror = null;
            this.socket.close();
            delete this.socket;
            this.socket = null;
        }
    }

    async createNewConnection(): Promise<void> {
        this.deleteConnection();

        this.socket = new WebSocket(this.url);

        this.socket.onmessage = ({ data, timeStamp }) => {
            this.store = {
                message: data,
                at: timeStamp,
            };
            this.dispatch();
        };

        this.socket.onopen = () => {
            this.retryTime = this.retryTimeStart;
            this.dispatch();
        };

        this.socket.onclose = async () => {
            this.retryConnection();
        };

        this.socket.onerror = async () => {
            this.retryConnection();
        };
    }

    async retryConnection(now = false): Promise<void> {
        console.log("retryConnection", this.retryingConnection, this.url);

        if (this.retryingConnection) {
            return;
        }

        this.retryingConnection = true;

        const delayTime =
            this.retryTime + Math.random() * this.retryTimeJitter;

        this.retryTime *= this.retryTimeMult;
        this.retryTime = Math.min(this.retryTime, this.maxRetrieTime);

        console.log("now", now, "this.retryTime", this.retryTime);

        if (now) {
            this.retryTime = 0;
        } else {
            await delay(delayTime);
        }

        if (this.socket && this.socket.readyState == WebSocket.CLOSED) {
            this.createNewConnection();
        }

        this.retryingConnection = false;
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
                this.deleteConnection();
                stores[this.url] = null;
                delete stores[this.url];
                stopWatchDog();
            }
        };
    }
}

type WSSubscriptionStoreMap = {
    [key: string]: WSSubscriptionStore;
};

const stores: WSSubscriptionStoreMap = {};

export function getSubscriptionFor(url: string): WSSubscriptionStore {
    if (!browser) {
        return null;
    }
    if (!stores[url]) {
        stores[url] = new WSSubscriptionStore(url);
    }
    return stores[url];
}

let watchDogTimer = null;
let watchDogLastTime = 0;
const watchDogInterval = 1000;
function startWatchDog(): void {
    if (!browser) {
        return;
    }
    if (watchDogLastTime == 0) {
        watchDogLastTime = Date.now();
    }
    clearInterval(watchDogTimer);
    watchDogTimer = setInterval(() => {
        const now = Date.now();
        // const deltaTime = now - watchDogLastTime;
        watchDogLastTime = now;

        // if (deltaTime > watchDogInterval * 2) {
        //     for (const url in stores) {
        //         const wsss = stores[url];
        //         if (wsss) {
        //             wsss.retryConnection(true);
        //         }
        //     }
        // }

        checkAllConnectionStatus();
    }, watchDogInterval);
}
function stopWatchDog(): void {
    let connectionActive = false;
    for (const url in stores) {
        if (stores[url]) {
            connectionActive = true;
        }
        break;
    }
    if (!connectionActive) {
        clearInterval(watchDogTimer);
    }
    checkAllConnectionStatus();
}

function checkAllConnectionStatus() {
    let activeWSS = 0;
    let activeCon = 0;

    // const readyMsgs = ["Connecitng", "OPEN", "Closing", "Closed"];
    for (const url in stores) {
        const wsss = stores[url];

        if (wsss) {
            activeWSS++;
            if (wsss.socket && wsss.socket.readyState <= WebSocket.OPEN) {
                activeCon++;
            }
        }
    }

    activeWSSubscriptions.set(activeWSS);
    activeWSConnections.set(activeCon);

    if (activeWSS != activeCon) {
        console.log("activeWSS", activeWSS, "activeCon", activeCon);

        for (const url in stores) {
            const wsss = stores[url];
            if (wsss) {
                console.log("wsss.url", wsss.url, url);
                wsss.retryConnection(true);
            }
        }
    }
}

if (browser) {
    window["checkAllConnectionStatus"] = checkAllConnectionStatus;
}
