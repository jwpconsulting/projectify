import type { Handle } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
    const response = await resolve(event, {
        // Potentially too broad
        // See https://github.com/sveltejs/kit/discussions/7027
        filterSerializedResponseHeaders: () => true,
    });

    return response;
};
