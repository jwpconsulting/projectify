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
import type { Invalidator, Subscriber, Unsubscriber } from "svelte/store";
import { writable } from "svelte/store";

import vars from "$lib/env";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    RepoGetter,
    SubscriptionType,
    WsResource,
} from "$lib/types/stores";

import { browser } from "$app/environment";

function makeAbsoluteUrl(url: string): string {
    if (!url.startsWith("/")) {
        return url;
    }
    const { host, protocol } = window.location;
    const wsProtocol = protocol === "https:" ? "wss://" : "ws://";
    return `${wsProtocol}${host}${url}`;
}

type EventListener = (resp: WsResponse) => void;
type ChangeListener = (change: unknown) => void;

let wsConnection: Sarus | undefined = undefined;

type Resource = "workspace" | "project" | "task";
type WsRequest =
    | { action: "subscribe"; resource: Resource; uuid: string }
    | { action: "unsubscribe"; resource: Resource; uuid: string };
type WsResponse =
    | {
          kind:
              | "alreadySubscribed"
              | "notSubscribed"
              | "notFound"
              | "gone"
              | "subscribed"
              | "unsubscribed";
          resource: Resource;
          uuid: string;
      }
    | { kind: "changed"; resource: Resource; uuid: string; content: unknown };

function dispatchMessage(event: MessageEvent<string>) {
    const message = JSON.parse(event.data) as WsResponse;
    const handled = [...listeners].some((listener) => {
        if (message.resource !== listener.resource) {
            return false;
        }
        if (message.uuid !== listener.uuid) {
            return false;
        }
        if (!listener.kind.includes(message.kind)) {
            return false;
        }
        listener.callback(message);
        return true;
    });
    if (!handled) {
        console.warn("Message not handled:", message);
    }
}

function sendWs(request: WsRequest) {
    if (wsConnection === undefined) {
        const url = makeAbsoluteUrl(`${vars.WS_ENDPOINT}/workspace/change`);
        wsConnection = new Sarus({
            url,
            eventListeners: {
                open: [() => console.debug("Connection opened to", url)],
                close: [() => console.debug("Connection closed to", url)],
                error: [() => console.error("Connection error for", url)],
                message: [dispatchMessage],
            },
        });
    }
    wsConnection.send(JSON.stringify(request));
}

interface Listener {
    resource: Resource;
    uuid: string;
    kind: WsResponse["kind"][];
    callback: EventListener;
}

const listeners = new Set<Listener>();

function addListener(listener: Listener) {
    if (listeners.has(listener)) {
        console.warn("Listener already added", listener);
    }
    listeners.add(listener);
}
function removeListener(listener: Listener) {
    if (!listeners.has(listener)) {
        console.warn("Listener already removed:", listener);
    }
    listeners.delete(listener);
};

async function unsubscribeFromCollection(resource: Resource, uuid: string) {
    if (wsConnection === undefined) {
        throw new Error("Expected wsConnection");
    }
    // TODO await confirmation
    console.debug(`unsubscribing from ${resource} and ${uuid}`);
    sendWs({ action: "unsubscribe", resource, uuid });
    const done = new Promise<void>((resolve) => {
        const disconnectedCb = (response: WsResponse) => {
            if (response.kind !== "unsubscribed") {
                console.debug("Still receiving messages for", resource, uuid);
                return;
            }
            console.debug("Unsubscribed from", resource, uuid);
            removeListener(listener);
            resolve();
        };
        const listener: Listener = {
            resource,
            uuid,
            kind: ["unsubscribed"],
            callback: disconnectedCb,
        };
        addListener(listener);
    });
    return await done;
}

async function getSubscriptionForCollection(
    resource: Resource,
    uuid: string,
    listener: ChangeListener,
): Promise<Unsubscriber> {
    const passMessageToListener = (response: WsResponse) => {
        if (response.kind === "changed") {
            listener(response.content);
        } else {
            console.warn(
                "Unhandled response when listening to subscription; ",
                response,
                `for resource ${resource} and uuid ${uuid}`,
            );
        }
    };
    const establishedConn = new Promise<Unsubscriber>((resolve, reject) => {
        const establishedConnectionCb = (response: WsResponse) => {
            if (response.kind === "notFound") {
                reject(new Error(`${uuid} not found`));
            }
            if (response.kind === "alreadySubscribed") {
                console.warn("Already subscribed to", resource, uuid);
            } else if (response.kind !== "subscribed") {
                console.warn("Don't know how to handle", response);
                return;
            } else {
                console.debug("Subscribed to", resource, uuid);
            }

            removeListener(subscribedListener);
            addListener(messageListener);
            resolve(async () => {
                console.debug("Cleaning up listener for", resource, uuid);
                removeListener(messageListener);
                await unsubscribeFromCollection(resource, uuid);
            });
        };
        const subscribedListener: Listener = {
            resource,
            uuid,
            kind: ["notFound", "alreadySubscribed", "subscribed"],
            callback: establishedConnectionCb,
        };
        const messageListener: Listener = {
            resource,
            uuid,
            kind: ["changed"],
            callback: passMessageToListener,
        };
        sendWs({
            action: "subscribe",
            resource,
            uuid,
        });
        addListener(subscribedListener);
    });
    return await establishedConn;
}

/* Subscribable WS Store
 *
 *  ┌─────┐   loadUuid  ┌─────┐ ──────────────┐
 *  │Start│────────────►│Ready│               │ subscription update:
 *  └─────┘             └─────┘ ◄─────────────┘ set(newValue)
 *                        ▲ │
 *                        │ │ loadUuid
 *                        │ │
 *                        └─┘
 *
 * This thing basically just passes on ws updates to subscribers, plus
 * one initial load
 */

type WsStoreState =
    | {
          collection: SubscriptionType;
          kind: "start";
      }
    | {
          collection: SubscriptionType;
          kind: "ready";
          uuid: string;
          unsubscriber: Unsubscriber;
      };

export function createWsStore<T>(
    collection: SubscriptionType,
    getter: RepoGetter<T>,
): WsResource<T> {
    type State = WsStoreState;
    let state: State = { collection, kind: "start" };
    const { subscribe: writeableSubscribe, set } = writable<T | undefined>(
        undefined,
    );

    const onMessage: ChangeListener = (changed: unknown) => {
        if (state.kind === "start") {
            throw new Error("State.kind is start");
        }
        set(changed as T);
    };

    const reset = () => {
        if (state.kind === "start") {
            console.warn("Already reset");
            return;
        }
        state.unsubscriber();
        state = { kind: "start", collection: state.collection };
    };

    const loadUuid = async (
        uuid: string,
        repositoryContext: RepositoryContext,
    ): Promise<T | undefined> => {
        if (state.kind === "ready" && uuid !== state.uuid) {
            // If we have already loaded a value:
            // First, we update all subscribers and tell them the current value
            // is undefined
            set(undefined);
        }
        // Fetch value early, since we need it either way
        const newValue = await getter(uuid, repositoryContext);
        // Then, when we find out we have already initialized for this uuid,
        // we can skip the queue and return early without cleaning up an
        // existing subscription.
        if (state.kind === "ready" && uuid === state.uuid) {
            set(newValue);
        } else {
            // On the other hand, if the uuid is changing, we need to unsubscribe
            // and create a new sub, as follows:
            // We need to unsubscribe from the old ws thing before adding
            // a new subscription here, if we are already initalized.
            if (state.kind === "ready") {
                state.unsubscriber();
            }
            const unsubscriber = await getSubscriptionForCollection(
                collection,
                uuid,
                onMessage,
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
            };
        }
        set(newValue);
        // And the caller of this method is definitely waiting for their result
        return newValue;
    };

    const subscribe = (
        run: Subscriber<T | undefined>,
        invalidate?: Invalidator<T | undefined> | undefined,
    ) => {
        const unsubscriber = writeableSubscribe(run, invalidate);
        return () => {
            if (state.kind === "ready") {
                reset();
            }
            unsubscriber();
        };
    };

    return { loadUuid, subscribe };
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
