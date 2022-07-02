import vars from "$lib/env";

export async function getWorkspaceBoard(uuid: string) {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/workspace-board/${uuid}`,
        { credentials: "include" }
    );
    return await response.json();
}
