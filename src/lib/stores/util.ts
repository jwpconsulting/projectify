import { derived, readonly, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";
import { browser } from "$app/environment";
import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

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

type UuidStore = Readable<string>;

export function createWsStore<T>(
    collection: "workspace" | "workspace-board" | "task",
    uuidReadable: UuidStore,
    getter: (uuid: string) => Promise<T>
): Readable<T | null> {
    const derive = ($uuidReadable: string, set: (t: T) => void) => {
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
            async (_value): Promise<void> => {
                console.log("Refetching thing", $uuidReadable);
                set(await getter($uuidReadable));
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
