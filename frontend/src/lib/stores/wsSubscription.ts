// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
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
import { writable } from "svelte/store";

import type {
    HasUuid,
    RepoGetter,
    SubscriptionType,
    WsResource,
    WsResourceContainer,
} from "$lib/types/stores";

import { browser } from "$app/environment";
import { backOff } from "exponential-backoff";

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
              | "already_subscribed"
              | "not_subscribed"
              | "not_found"
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
        const url = makeAbsoluteUrl(`${__WS_ENDPOINT__}/workspace/change`);
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
            if (response.kind === "not_subscribed") {
                console.warn("Never subscribed to", resource);
                return;
            }
            console.debug("Unsubscribed from", resource);
            removeListener(listener);
            resolve();
        };
        const listener: Listener = {
            resource,
            kind: ["unsubscribed", "not_subscribed"],
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

type AsyncUnsubscriber = () => Promise<void>;

async function subscribeToResource(
    resource: Resource,
    listener: EventListener,
    reconnect: Reconnector,
): Promise<AsyncUnsubscriber> {
    const messageListener: Listener = {
        resource,
        kind: ["gone", "changed"],
        callback: listener,
        reconnect: reconnect,
    };

    const unsubscribe = async () => {
        console.debug("Cleaning up listener for", resource);
        removeListener(messageListener);
        await unsubscribeFromResource(resource);
    };
    const established = new Promise<AsyncUnsubscriber>((resolve, reject) => {
        const establishedConnectionCb = (response: WsResponse) => {
            if (response.kind === "not_found") {
                reject(
                    new Error(
                        `Resource ${JSON.stringify(resource)} not found`,
                    ),
                );
                return;
            }
            if (response.kind === "already_subscribed") {
                console.warn("Already subscribed to", resource);
            }

            console.debug("Subscribed to", resource);
            removeListener(subscribedListener);
            addListener(messageListener);
            resolve(unsubscribe);
        };
        const subscribedListener: Listener = {
            resource,
            kind: ["not_found", "already_subscribed", "subscribed"],
            callback: establishedConnectionCb,
            reconnect() {
                console.warn("Reconnected while subscribing");
            },
        };
        addListener(subscribedListener);
    });
    sendWs({ action: "subscribe", ...resource });
    return await established;
}

/* Subscribable WS Store
 *
 *  ┌─────┐   loadUuid  ┌─────┐ ──────────────┐
 *  │Start│────────────►│Ready│               │ subscription update:
 *  └─────┘             └─────┘ ◄─────────────┘ set(newValue)
 *                        ▲ │
 *                        │ │ loadUuid
 *                        │ │ reconnect
 *                        └─┘
 *
 * This thing basically just passes on ws updates to subscribers, plus
 * one initial load
 */

type WsStoreState<T> =
    | {
          kind: "start";
      }
    | {
          kind: "loading";
          uuid: string;
      }
    | {
          kind: "ready";
          uuid: string;
          unsubscriber: AsyncUnsubscriber;
          value: T | undefined;
      };

export function createWsStore<T extends HasUuid>(
    resource: SubscriptionType,
    getter: RepoGetter<T>,
): WsResource<T> {
    type State = WsStoreState<T>;
    let state: State = { kind: "start" };

    const { subscribe, set } = writable<WsResourceContainer<T>>(
        {
            or: (t: T) => t,
            orPromise: (t: Promise<T>) => t,
            value: undefined,
        },
        () => stop,
    );

    const reset = () => {
        set({
            or: (t: T) => t,
            orPromise: (t: Promise<T>) => t,
            value: undefined,
        });
        state = { kind: "start" };
    };

    const resetAndUnsubscribe = async () => {
        if (state.kind === "start") {
            console.warn("Already reset");
            return;
        }
        if (state.kind === "loading") {
            console.warn("Tried to reset while loading");
            return;
        }
        console.debug("Resetting");
        await state.unsubscriber();
        reset();
    };

    const stop = () => {
        if (state.kind === "start") {
            return;
        }
        console.debug("Stopping");
        resetAndUnsubscribe().catch((error: unknown) =>
            console.error("Error when resetting", error),
        );
    };

    const onMessage: EventListener = (resp: WsResponse) => {
        if (state.kind === "start") {
            throw new Error("State.kind is start");
        }
        if (state.kind === "loading") {
            throw new Error("Received message while loading");
        }
        if (resp.kind === "gone") {
            reset();
        } else if (resp.kind === "changed") {
            const value = resp.content as T;
            set({
                or: () => value,
                value,
                orPromise: () => Promise.resolve(value),
            });
        } else {
            throw new Error("resp.kind is not 'changed'");
        }
    };

    const reconnect: Reconnector = async () => {
        if (state.kind !== "ready") {
            throw new Error("Trying to reconnect, despite not being ready");
        }
        console.warn("Connection closed, reconnecting");
        const { uuid } = state;
        const unsubscriber = await subscribeToResource(
            { resource, uuid },
            onMessage,
            reconnect,
        );
        console.debug("Reconnected");
        state = { ...state, unsubscriber };
    };

    const loadUuid = async (uuid: string): Promise<T | undefined> => {
        if (state.kind === "ready" && uuid !== state.uuid) {
            // If we have already loaded a value:
            // First, we update all subscribers and tell them the current value
            // is undefined
            set({
                or: (t: T) => t,
                value: undefined,
                orPromise: (t: Promise<T>) => t,
            });
        }
        // If we are reloading the same uuid, we don't need to resubscribe
        const alreadySubscribedToUuid =
            state.kind === "ready" && uuid === state.uuid;
        // On the other hand, if the uuid is changing and we are in a "ready"
        // state, we need to unsubscribe.
        // We need to unsubscribe from the old ws thing before adding
        // a new subscription here, if we are already initalized.
        if (state.kind === "ready" && uuid !== state.uuid) {
            console.log("Unsubscribing", state);
            await state.unsubscriber();
        }
        // But we still need to rememember that we are loading
        state = { kind: "loading", uuid };
        // TODO inform subscribers that we are loading
        // Fetch value early, since we need it either way
        const value: T | undefined = await backOff(() => getter(uuid));
        // If nothing was returned we can return early. Otherwise we will start
        // subscribing to a resource that does not exist
        if (value === undefined) {
            set({
                or: (t: T) => t,
                orPromise: (t: Promise<T>) => t,
                value: undefined,
            });
            return undefined;
        }
        // Then, when we find out we have already initialized for this uuid,
        // we can skip the queue and return early without cleaning up an
        // existing subscription.
        if (alreadySubscribedToUuid) {
            set({
                or: () => value,
                orPromise: () => Promise.resolve(value),
                value,
            });
            return value;
        }

        // In this branch, we know that the previous uuid subscribed to was
        // different, or we haven't subscribed to anything at all.
        const unsubscriber = await subscribeToResource(
            { resource, uuid },
            onMessage,
            reconnect,
        );
        state = {
            ...state,
            kind: "ready",
            uuid,
            unsubscriber,
            value,
        };
        set({
            or: () => value,
            orPromise: () => Promise.resolve(value),
            value,
        });
        // And the caller of this method is definitely waiting for their result
        return value;
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
