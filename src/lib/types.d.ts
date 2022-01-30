/**
 * Can be made globally available by placing this
 * inside `global.d.ts` and removing `export` keyword
 */
export interface Locals {
    userid: string;
}

declare namespace svelte.JSX {
    interface HTMLAttributes<T> {
        ondragClick: () => void;
    }
}
