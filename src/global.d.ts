/// <reference types="@sveltejs/kit" />
declare namespace svelte.JSX {
    interface HTMLAttributes<T> {
        ondragClick?: (event: any) => any;
        ondragStart?: (event: any) => any;
        ondragEnd?: (event: any) => any;
    }
}

declare module "daisyui/colors/colorNames.js";
declare module "daisyui/colors/hex2hsl.js";
