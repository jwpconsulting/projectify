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
    RepoGetter,
    SubscriptionType,
    WsResource,
} from "$lib/types/stores";

import { browser } from "$app/environment";

interface Message {
    type: string;
    uuid: string;
    data: unknown;
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
    onMessage: EventListener,
): Unsubscriber {
    // XXX
    // It appears that errors here are very hard to debug,
    // e.g., wrong URL schema
    // Check if we have a relative URL
    const url = makeAbsoluteUrl(`${vars.WS_ENDPOINT}/${collection}/${uuid}/`);
    try {
        const sarus = new Sarus({
            url,
            eventListeners: {
                open: [() => console.debug("Connection opened to", url)],
                close: [() => console.debug("Connection closed to", url)],
                error: [() => console.error("Connection error for", url)],
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
    const { subscribe, set } = writable<T | undefined>(undefined);

    const onMessage: EventListener = (event: MessageEvent<string>) => {
        const message: Message = JSON.parse(event.data) as Message;
        if (state.kind === "start") {
            throw new Error("State.kind is start");
        }
        set(message.data as T);
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
            const unsubscriber = getSubscriptionForCollection(
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
