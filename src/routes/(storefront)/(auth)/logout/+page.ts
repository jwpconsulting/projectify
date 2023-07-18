import { logout } from "$lib/stores/user";

export const prerender = false;
export const ssr = false;

export async function load() {
    await logout();
}
