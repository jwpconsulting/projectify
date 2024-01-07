// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import Sarus from "@anephenix/sarus";
import type { Unsubscriber } from "svelte/store";
import { writable } from "svelte/store";

import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    MaybeSubscriber,
    RepoGetter,
    SubscriptionType,
    WsResource,
} from "$lib/types/stores";
import { unwrap } from "$lib/utils/type";

import { browser } from "$app/environment";

interface Message {
    type: string;
    uuid: string;
    data: unknown;
}

interface WsMessage {
    message: Message;
    timeStamp: number;
}

function makeAbsoluteUrl(url: string): string {
    if (!url.startsWith("/")) {
        return url;
    }
    const { host, protocol } = window.location;
    const wsProtocol = protocol === "https:" ? "wss://" : "ws://";
    return `${wsProtocol}${host}${url}`;
}

type EventListener = (event: MessageEvent<string>) => void;

function getSubscriptionForCollection(
    collection: string,
    uuid: string,
    onWsMessage: (wsMessage: WsMessage) => void,
): Unsubscriber {
    const onMessage: EventListener = (event: MessageEvent<string>) => {
        const message: Message = JSON.parse(event.data) as Message;
        const { timeStamp } = event;
        onWsMessage({ message, timeStamp });
    };
    // XXX
    // It appears that errors here are very hard to debug,
    // e.g., wrong URL schema
    // Check if we have a relative URL
    const url = makeAbsoluteUrl(`${vars.WS_ENDPOINT}/${collection}/${uuid}/`);
    try {
        const sarus = new Sarus({
            url,
            eventListeners: {
                open: [console.debug.bind(null, "Connection opened to", url)],
                close: [console.debug.bind(null, "Connection closed to", url)],
                error: [console.error.bind(null, "Connection error for", url)],
                message: [onMessage],
            },
        });
        return () => sarus.disconnect();
    } catch (e) {
        console.error("When initializing Sarus", e);
        throw e;
    }
}

/* Subscribable WS Store
 *
 *  ┌─────┐   loadUuid  ┌─────┐ ──────────────┐
 *  │Start│────────────►│Ready│               │ subscription update:
 *  └─────┘             └─────┘ ◄─────────────┘ updateSubscribers()
 *                        ▲ │
 *                        │ │ loadUuid
 *                        │ │
 *                        └─┘
 *
 * This thing basically just passes on ws updates to subscribers, plus
 * one initial load
 */

type Subscribers<T> = Set<MaybeSubscriber<T>>;
type WsStoreState<T> =
    | {
          collection: SubscriptionType;
          kind: "start";
          subscribers: Subscribers<T>;
      }
    | {
          collection: SubscriptionType;
          kind: "ready";
          uuid: string;
          subscribers: Subscribers<T>;
          unsubscriber: Unsubscriber;
          value: T | undefined;
      };

// TODO warn when this store never updates a subscriber
// warn when this store deinitializes without ever adding a subscriber
export function createWsStore<T>(
    collection: SubscriptionType,
    getter: RepoGetter<T>,
): WsResource<T> {
    type State = WsStoreState<T>;
    let state: State = { collection, kind: "start", subscribers: new Set() };

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

    const updateSubscribers = (state: State & { kind: "ready" }) => {
        state.subscribers.forEach((subscriber) => subscriber(state.value));
    };

    const removeSubscriber = (subscriber: MaybeSubscriber<T>) => {
        state.subscribers.delete(subscriber);
        // This could be an edge case, since we don't return to start, ever.
        // So when someone subscribes and unsubscribes, that means a component
        // or similar was unloaded prematurely. For this reason, we log that
        // here until we gain some more insight on this issue.
        if (state.kind === "start") {
            console.log(
                `Removed subscriber for ${collection} collection before store was ever initialized`,
            );
            return;
        }
    };

    const loadUuid = async (
        uuid: string,
        repositoryContext: RepositoryContext,
    ): Promise<T | undefined> => {
        // Fetch value early, since we need it either way
        const value = await getter(uuid, repositoryContext);
        // Then, when we find out we have already initialized for this uuid,
        // we can skip the queue and return early without cleaning up an
        // existing subscription.
        if (state.kind === "ready" && uuid === state.uuid) {
            state = {
                ...state,
                value,
            };
        } else {
            // On the other hand, if the uuid is changing, we need to unsubscribe
            // and create a new sub, as follows:
            // We need to unsubscribe from the old ws thing before adding
            // a new subscription here, if we are already initalized.
            if (state.kind === "ready") {
                state.unsubscriber();
            }
            const unsubscriber = getSubscriptionForCollection(
                collection,
                uuid,
                receiveWsMessage,
            );
            // Since further reloads are independent of any fetch (the data comes
            // from ws), we don't have to store the repositoryContext as part of
            // the state. It's important that we don't reuse a user supplied
            // fetch (aka repositoryContext) after page navigation, since in server
            // side mode this is not guaranteed to work: SvelteKit might unload it.
            state = {
                ...state,
                kind: "ready",
                uuid,
                unsubscriber,
                value,
            };
        }
        // Either way, we absolutely need to update our subscribers.
        updateSubscribers(state);
        // And the caller of this method is definitely waiting for their result
        return value;
    };

    return {
        loadUuid,
        subscribe(run: MaybeSubscriber<T>): Unsubscriber {
            // This is surprisingly easy to implement!
            // https://github.com/sveltejs/svelte/blob/8e76ef156e2bdd2a1e7a506a593c2d5f58c498b5/packages/svelte/src/runtime/store/index.js#L86
            state.subscribers.add(run);
            // If we have nothing, return undefined
            run(state.kind === "ready" ? state.value : undefined);
            return () => removeSubscriber(run);
        },
        unwrap(): T {
            if (state.kind !== "ready") {
                throw new Error("Store wasn't ready");
            }
            return unwrap(state.value, "Expected state.value to be present");
        },
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
