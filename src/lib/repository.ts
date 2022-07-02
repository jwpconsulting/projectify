import vars from "$lib/env";

export async function getUser() {
    const response = await fetch(`${vars.API_ENDPOINT}/user/user`, {
        credentials: "include",
    });
    return await response.json();
}

export async function getWorkspaceBoard(uuid: string) {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/workspace-board/${uuid}`,
        { credentials: "include" }
    );
    return await response.json();
}
