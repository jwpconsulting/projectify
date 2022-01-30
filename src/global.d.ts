/// <reference types="@sveltejs/kit" />
declare namespace svelte.JSX {
    interface HTMLAttributes<T> {
        ondragClick?: (event: any) => any;
    }
}
