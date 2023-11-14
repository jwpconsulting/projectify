import type { PageLoadEvent } from "./$types";

interface Data {
    email: string;
    token: string;
}
export function load({ params: { email, token } }: PageLoadEvent): Data {
    return { email, token };
}
