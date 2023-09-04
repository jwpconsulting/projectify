import { logout } from "$lib/stores/user";

export async function load() {
    await logout();
}
