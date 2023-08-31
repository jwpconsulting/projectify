import Fuse from "fuse.js";
import { derived, readonly, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { fuseSearchThreshold } from "$lib/config";
import vars from "$lib/env";

import { browser } from "$app/environment";
import { getSubscriptionFor } from "$lib/stores/wsSubscription";
import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
import type { RecursiveKeyOf, SearchInput } from "$lib/types/base";
import type { SubscriptionType, WsResource } from "$lib/types/stores";

type Unsubscriber = () => void;

type MaybeUuid = string | null;
// Maybe make a read only UuidStore type for our derivation step
type UuidStore = Writable<MaybeUuid>;

const getSubscriptionForCollection = (
    collection: "workspace" | "workspace-board" | "task",
    uuid: string
): WSSubscriptionStore | null => {
    let wsEndPoint = vars.WS_ENDPOINT;
    if (wsEndPoint.startsWith("/ws")) {
        wsEndPoint = `ws://${location.host}${wsEndPoint}`;
    }
    const wsURL = `${wsEndPoint}/${collection}/${uuid}/`;

    return getSubscriptionFor(wsURL);
};

export function createWsStore<T>(
    collection: SubscriptionType,
    uuidReadable: UuidStore,
    getter: (uuid: string) => Promise<T>
): WsResource<T> {
    let setHack: ((t: T) => void) | undefined = undefined;
    const derive = ($uuidReadable: MaybeUuid, set: (t: T) => void) => {
        // If the uuid changes, does that mean we have to force unsubscribe
        // from WS here?
        // Justus 2023-08-31
        // TODO: Research
        setHack = set;
        if (!browser) {
            return;
        }
        if (!$uuidReadable) {
            return;
        }
        getter($uuidReadable)
            .then((result) => set(result))
            .catch((error: Error) => {
                console.error("Failure when trying to get initialing thing", {
                    error,
                });
            });
        const subscription = getSubscriptionForCollection(
            collection,
            $uuidReadable
        );
        if (!subscription) {
            throw new Error("Expected subscription");
        }
        const unsubscriber: Unsubscriber = subscription.subscribe(
            ({ message }): void => {
                const thing: T = message.data as T;
                console.log("The thing is now", thing);
                set(thing);
            }
        );
        // Supposedly, return this function will allow svelte/store
        // to call this when the derived store is unsubscribed fully
        // TODO test this
        return unsubscriber;
    };
    const loadUuid = async (uuid: string): Promise<T> => {
        const it = await getter(uuid);
        // We want setHack to be there, but it's not on an initial pageload
        // In the future, we just hide current*Uuid from the user
        // Then we have all the freedom to do what we want to
        if (!setHack) {
            // This will trigger a load twice, maybe?
            // Or svelte store is intelligent enough to notice that the
            // uuid is the same, then maybe not...
            uuidReadable.set(uuid);
            console.error("We rely on a hack, and the hack did not work :(");
        } else {
            setHack(it);
        }
        return it;
    };
    const { subscribe }: Readable<T | null> = derived<UuidStore, T | null>(
        uuidReadable,
        derive,
        null
    );
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
