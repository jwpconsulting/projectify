import Sarus from "@anephenix/sarus";
import type { Unsubscriber, Subscriber, Readable } from "svelte/store";
import { writable } from "svelte/store";

import vars from "$lib/env";

import { browser } from "$app/environment";
import type { SubscriptionType, WsResource } from "$lib/types/stores";

interface Message {
    type: string;
    uuid: string;
    data: unknown;
}

interface WsMessage {
    message: Message;
    timeStamp: number;
}

// A svelte store subscriber that received WSMessages
type WsSubscriber = Subscriber<WsMessage>;

const wsSubscriptionStores = new Map<string, WsSubscriptionStore>();

type WsSubscriptionStore = Readable<WsMessage>;

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

function getSubscriptionFor(url: string): WsSubscriptionStore {
    const store = wsSubscriptionStores.get(url);
    if (store) {
        return store;
    }
    const newStore: WsSubscriptionStore = makeWsSubscriptionStore(url);
    wsSubscriptionStores.set(url, newStore);
    return newStore;
}

export function getSubscriptionForCollection(
    collection: string,
    uuid: string
): WsSubscriptionStore {
    let wsEndPoint = vars.WS_ENDPOINT;
    if (wsEndPoint.startsWith("/ws")) {
        wsEndPoint = `ws://${location.host}${wsEndPoint}`;
    }
    const wsURL = `${wsEndPoint}/${collection}/${uuid}/`;

    return getSubscriptionFor(wsURL);
}

/* Subscribable WS Store
 *
 *  ┌─────┐   loadUuid  ┌─────┐ ──────────────┐
 *  │Start│────────────►│Ready│               │ subscription update:
 *  └─────┘             └─────┘ ◄─────────────┘ updateSubscribers()
 *
 * This thing basically just passes on ws updates to subscribers, plus
 * one initial load
 */

type Subscribers<T> = Set<Subscriber<T>>;
type WsStoreState<T> =
    | { kind: "start"; subscribers: Subscribers<T> }
    | {
          kind: "ready";
          uuid: string;
          subscribers: Subscribers<T>;
          unsubscriber: Unsubscriber;
          value: T;
      };

export function createWsStore<T>(
    collection: SubscriptionType,
    getter: (uuid: string) => Promise<T>
): WsResource<T> {
    type State = WsStoreState<T>;
    let state: State = { kind: "start", subscribers: new Set() };

    const receiveWsMessage = (message: WsMessage): void => {
        if (state.kind === "start") {
            throw new Error("State.kind is start");
        }
        const value: T = message.message.data as T;
        state = {
            ...state,
            value,
        };
        updateSubscribers(state);
    };

    const loadSubscription = (uuid: string): Unsubscriber => {
        const store = getSubscriptionForCollection(collection, uuid);
        return store.subscribe(receiveWsMessage);
    };

    const updateSubscribers = (state: State & { kind: "ready" }) => {
        state.subscribers.forEach((subscriber) => subscriber(state.value));
    };

    const removeSubscriber = (subscriber: Subscriber<T>) => {
        state.subscribers.delete(subscriber);
        if (state.subscribers.size > 0) {
            return;
        }
        if (state.kind === "start") {
            return;
        }
        state.unsubscriber();
        state = {
            kind: "start",
            subscribers: state.subscribers,
        };
    };

    const loadUuid = async (uuid: string): Promise<T> => {
        // We need to unsubscribe from the old ws thing before adding
        // a new subscription here.
        if (state.kind === "ready") {
            state.unsubscriber();
        }
        const unsubscriber = loadSubscription(uuid);
        const value = await getter(uuid);
        state = { ...state, kind: "ready", uuid, unsubscriber, value };
        updateSubscribers(state);
        return value;
    };

    const subscribe = (run: Subscriber<T>): Unsubscriber => {
        // This is surprisingly easy to implement!
        // https://github.com/sveltejs/svelte/blob/8e76ef156e2bdd2a1e7a506a593c2d5f58c498b5/packages/svelte/src/runtime/store/index.js#L86
        state.subscribers.add(run);
        if (state.kind === "ready") {
            run(state.value);
        } else {
            console.debug("Subscribed", run, "but no value there yet");
        }
        return () => removeSubscriber(run);
    };
    return {
        subscribe,
        loadUuid,
    };
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
