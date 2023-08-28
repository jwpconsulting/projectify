import Fuse from "fuse.js";
import { derived, readonly, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { fuseSearchThreshold } from "$lib/config";

import { browser } from "$app/environment";
import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
import type { SubscriptionType } from "$lib/types/stores";

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

type Unsubscriber = () => void;

type MaybeUuid = string | null;
type UuidStore = Readable<MaybeUuid>;

export function createWsStore<T>(
    collection: SubscriptionType,
    uuidReadable: UuidStore,
    getter: (uuid: string) => Promise<T>
): Readable<T | null> {
    const derive = ($uuidReadable: MaybeUuid, set: (t: T) => void) => {
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
    const { subscribe }: Readable<T | null> = derived<UuidStore, T | null>(
        uuidReadable,
        derive,
        null
    );
    return {
        subscribe,
    };
}

export function searchAmong<T>(
    keys: (keyof T & string)[],
    things: T[],
    searchText: string
): T[] {
    // If there is nothing to search for, we return everything
    // But it would be better if we had some kind of guaranteed non-empty
    // string as an input here
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
