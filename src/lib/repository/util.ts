import vars from "$lib/env";

import { browser } from "$app/environment";

import type { RepositoryContext } from "$lib/types/repository";

const defaultRepositoryContext: RepositoryContext | null = browser
    ? {
          fetch: window.fetch,
      }
    : null;

export async function getWithCredentialsJson<T>(
    url: string,
    repositoryContext: RepositoryContext | null = defaultRepositoryContext
): Promise<T> {
    if (!repositoryContext) {
        throw new Error("Expected repositoryContext");
    }
    const { fetch } = repositoryContext;
    const response = await fetch(`${vars.API_ENDPOINT}${url}`, {
        credentials: "include",
    });
    const body = await response.json();
    if (!response.ok) {
        throw new Error(`${response.statusText}: ${JSON.stringify(body)}`);
    }
    return body;
}
