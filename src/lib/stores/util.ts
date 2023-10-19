import Fuse from "fuse.js";
import { readonly, writable } from "svelte/store";
import type { Readable, Writable } from "svelte/store";

import { fuseSearchThreshold } from "$lib/config";
import type { RecursiveKeyOf, SearchInput } from "$lib/types/base";

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
