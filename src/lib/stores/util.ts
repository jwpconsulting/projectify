import { readonly, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

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
