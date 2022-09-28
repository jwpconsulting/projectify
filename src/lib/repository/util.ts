import vars from "$lib/env";

export async function getWithCredentialsJson<T>(url: string): Promise<T> {
    const response = await fetch(`${vars.API_ENDPOINT}${url}`, {
        credentials: "include",
    });
    const body = await response.json();
    if (!response.ok) {
        throw new Error(`${response.statusText}: ${JSON.stringify(body)}`);
    }
    return body;
}
