import { logOut } from "$lib/stores/user";

export async function load() {
    await logOut();
}
