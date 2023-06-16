import type { LayoutLoadEvent } from "./$types";

interface Data {
    redirectTo: string | undefined;
}

export const prerender = false;

export function load({ url }: LayoutLoadEvent): Data {
    const redirectTo = url.searchParams.get("next") ?? undefined;
    return {
        redirectTo,
    };
}
