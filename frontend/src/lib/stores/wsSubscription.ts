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

type WsRequest =
    | { action: "subscribe"; resource: SubscriptionType; uuid: string }
    | { action: "unsubscribe"; resource: SubscriptionType; uuid: string };
type WsResponse =
    | {
          kind:
              | "alreadySubscribed"
              | "notSubscribed"
              | "notFound"
              | "gone"
              | "subscribed"
              | "unsubscribed";
          resource: SubscriptionType;
          uuid: string;
      }
    | {
          kind: "changed";
          resource: SubscriptionType;
          uuid: string;
          content: unknown;
      };

function onMessage(event: MessageEvent<string>) {
    const message = JSON.parse(event.data) as WsResponse;
    const handled = [...listeners].some((listener) => {
        if (message.resource !== listener.resource.resource) {
            return false;
        }
        if (message.uuid !== listener.resource.uuid) {
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

type ConnectionState =
    | { kind: "undefined" }
    | {
          kind: "connecting" | "opened" | "closed" | "reopened" | "errored";
          sarus: Sarus;
      };

let connectionState: ConnectionState = { kind: "undefined" };

function onOpen(_event: Event) {
    if (connectionState.kind === "connecting") {
        console.debug("Connection opened");
        connectionState.kind = "opened";
    } else if (connectionState.kind === "closed") {
        console.debug("Connection reopened");
        connectionState.kind = "reopened";
        const reconnectingListeners = [...listeners];
        // We flush the listeners, since otherwise we'd try to unsubscribe
        // the old "changed" listeners
        listeners.clear();

        reconnectingListeners.forEach((listener) => {
            console.debug("Trying to reconnect", listener);
            listener.reconnect();
        });
    }
}

function onClose(_event: Event) {
    console.debug("Connection closed");
    connectionState.kind = "closed";
}

function onError(event: Event) {
    console.error("Error", event);
    connectionState.kind = "errored";
}

function sendWs(request: WsRequest) {
    if (connectionState.kind === "undefined") {
        const url = makeAbsoluteUrl(`${vars.WS_ENDPOINT}/workspace/change`);
        const sarus = new Sarus({
            url,
            eventListeners: {
                open: [onOpen],
                close: [onClose],
                error: [onError],
                message: [onMessage],
            },
        });
        connectionState = {
            kind: "connecting",
            sarus,
        };
    }
    connectionState.sarus.send(JSON.stringify(request));
}

interface Listener {
    resource: Resource;
    kind: WsResponse["kind"][];
    callback: EventListener;
    reconnect: Reconnector;
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
}

interface Resource {
    resource: SubscriptionType;
    uuid: string;
}

async function unsubscribeFromResource(resource: Resource) {
    console.debug("Unsubscribing from", resource);
    sendWs({ action: "unsubscribe", ...resource });
    const done = new Promise<void>((resolve) => {
        const disconnectedCb = (response: WsResponse) => {
            if (response.kind !== "unsubscribed") {
                console.debug("Still receiving messages for", resource);
                return;
            }
            console.debug("Unsubscribed from", resource);
            removeListener(listener);
            resolve();
        };
        const listener: Listener = {
            resource,
            kind: ["unsubscribed"],
            callback: disconnectedCb,
            reconnect() {
                console.warn("Reconnected while unsubscribing");
            },
        };
        addListener(listener);
    });
    return await done;
}

type Reconnector = () => void;

async function subscribeToResource(
    resource: Resource,
    listener: EventListener,
    onReconnect: Reconnector,
): Promise<Unsubscriber> {
    const messageListener: Listener = {
        resource,
        kind: ["changed"],
        callback: listener,
        reconnect: onReconnect,
    };

    const unsubscribe = async () => {
        console.debug("Cleaning up listener for", resource);
        removeListener(messageListener);
        await unsubscribeFromResource(resource);
    };
    const establishedConn = new Promise<Unsubscriber>((resolve, reject) => {
        const establishedConnectionCb = (response: WsResponse) => {
            if (response.kind === "notFound") {
                reject(
                    new Error(
                        `Resource ${JSON.stringify(resource)} not found`,
                    ),
                );
            }
            if (response.kind === "alreadySubscribed") {
                console.warn("Already subscribed to", resource);
            } else {
                console.debug("Subscribed to", resource);
            }

            removeListener(subscribedListener);
            addListener(messageListener);
            resolve(unsubscribe);
        };
        const subscribedListener: Listener = {
            resource,
            kind: ["notFound", "alreadySubscribed", "subscribed"],
            callback: establishedConnectionCb,
            reconnect() {
                console.warn("Reconnected while subscribing");
            },
        };
        addListener(subscribedListener);
    });
    sendWs({ action: "subscribe", ...resource });
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
          subscriptionType: SubscriptionType;
          kind: "start";
      }
    | {
          subscriptionType: SubscriptionType;
          kind: "ready";
          uuid: string;
          unsubscriber: Unsubscriber;
      };

export function createWsStore<T>(
    subscriptionType: SubscriptionType,
    getter: RepoGetter<T>,
): WsResource<T> {
    type State = WsStoreState;
    let state: State = { subscriptionType, kind: "start" };
    const { subscribe: writeableSubscribe, set } = writable<T | undefined>(
        undefined,
    );

    const onMessage: EventListener = (resp: WsResponse) => {
        if (resp.kind !== "changed") {
            throw new Error("resp.kind is not changed");
        }
        if (state.kind === "start") {
            throw new Error("State.kind is start");
        }
        set(resp.content as T);
    };

    const onReconnect: Reconnector = async () => {
        if (state.kind !== "ready") {
            throw new Error("Trying to reconnect, despite not being ready");
        }
        console.warn("Connection closed, reconnecting");
        const { subscriptionType: resource, uuid } = state;
        const unsubscriber = await subscribeToResource(
            { resource, uuid },
            onMessage,
            onReconnect,
        );
        console.debug("Reconnected");
        state = {
            ...state,
            unsubscriber,
        };
    };

    const reset = () => {
        if (state.kind === "start") {
            console.warn("Already reset");
            return;
        }
        state.unsubscriber();
        state = { kind: "start", subscriptionType: state.subscriptionType };
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
            const unsubscriber = await subscribeToResource(
                { resource: subscriptionType, uuid },
                onMessage,
                onReconnect,
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
