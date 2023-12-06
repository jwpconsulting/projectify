import { writable } from "svelte/store";

import { goto } from "$lib/navigation";
import { getUser, updateUser } from "$lib/repository/user";
import * as userRepository from "$lib/repository/user";
import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";

export const user = writable<User | undefined>(undefined);

// TODO rename this to logIn
export async function login(
    email: string,
    password: string,
    redirectTo: string | undefined,
    repositoryContext: RepositoryContext
): Promise<void> {
    const response = await userRepository.logIn(
        email,
        password,
        repositoryContext
    );
    user.set(response);

    if (redirectTo) {
        await goto(redirectTo);
    }
}

export async function logOut(repositoryContext: RepositoryContext) {
    await userRepository.logOut(repositoryContext);
    user.set(undefined);
}

export async function fetchUser(
    repositoryContext: RepositoryContext
): Promise<User | undefined> {
    const userData = await getUser(repositoryContext);
    user.set(userData);
    return userData;
}

export async function updateUserProfile(
    // TODO fullName -> displayName
    fullName: string | undefined,
    repositoryContext: RepositoryContext
) {
    await updateUser({ full_name: fullName }, repositoryContext);
    // We fetch the user to make sure the full name is updated
    // Ideally, this would just store the result of the above operation
    // in the user store
    await fetchUser(repositoryContext);
}
