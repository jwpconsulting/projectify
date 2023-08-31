import Fuse from "fuse.js";
import { readonly, writable } from "svelte/store";
import type {
    Subscriber,
    Readable,
    Writable,
    Unsubscriber,
} from "svelte/store";

import { fuseSearchThreshold } from "$lib/config";
import vars from "$lib/env";

import { getSubscriptionFor } from "$lib/stores/wsSubscription";
import type {
    WsSubscriptionStore,
    WsMessage,
} from "$lib/stores/wsSubscription";
import type { RecursiveKeyOf, SearchInput } from "$lib/types/base";
import type { SubscriptionType, WsResource } from "$lib/types/stores";

const getSubscriptionForCollection = (
    collection: "workspace" | "workspace-board" | "task",
    uuid: string
): WsSubscriptionStore | null => {
    let wsEndPoint = vars.WS_ENDPOINT;
    if (wsEndPoint.startsWith("/ws")) {
        wsEndPoint = `ws://${location.host}${wsEndPoint}`;
    }
    const wsURL = `${wsEndPoint}/${collection}/${uuid}/`;

    return getSubscriptionFor(wsURL);
};

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
        const subscription = getSubscriptionForCollection(collection, uuid);
        if (!subscription) {
            throw new Error("Expected subscription");
        }
        return subscription.subscribe(receiveWsMessage);
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

export function searchAmong<T extends object>(
    keys: RecursiveKeyOf<T>[],
    things: T[],
    searchText: SearchInput
): T[] {
    // If there is nothing to search for, we return everything
    // But it would be better if we had some kind of guaranteed non-empty
    // string as an input here
    if (searchText === undefined) {
        return things;
    }
    if (searchText.length === 0) {
        return things;
    }
    const searchEngine = new Fuse<T>(things, {
        keys: keys,
        threshold: fuseSearchThreshold,
    });

    return searchEngine
        .search(searchText)
        .map((res: Fuse.FuseResult<T>) => res.item);
}

export function internallyWritable<T>(theThing: T): {
    pub: Readable<T>;
    priv: Writable<T>;
} {
    const priv = writable(theThing);
    const pub = readonly(priv);
    return {
        priv,
        pub,
    };
}
