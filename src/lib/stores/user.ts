import { writable } from "svelte/store";

import { client } from "$lib/graphql/client";
import { goto } from "$lib/navigation";
import { getUser, updateUser } from "$lib/repository/user";
import * as userRepository from "$lib/repository/user";
import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";

// TODO export const user = writable<User | undefined>(undefined);
export const user = writable<User | null>(null);

// TODo rename this
export const login = async (
    email: string,
    password: string,
    redirectTo?: string
): Promise<void> => {
    const response = await userRepository.logIn(email, password, { fetch });
    user.set(response);

    if (redirectTo) {
        await goto(redirectTo);
    }
};

export const logOut = async () => {
    // TODO add repository context
    await userRepository.logOut({ fetch });
    // TODO remove apollo
    await client.resetStore();
    user.set(null);
};

// TODO return | undefined
export const fetchUser = async (
    repositoryContext: RepositoryContext
): Promise<User | null> => {
    const userData = await getUser(repositoryContext);
    if (!userData) {
        return null;
    }
    user.set(userData);
    return userData;
};

// TODO add repo argument
export const requestPasswordReset = async (email: string): Promise<void> => {
    await userRepository.requestPasswordReset(email, { fetch });
};

// TODO add repo argument
export const confirmPasswordReset = async (
    email: string,
    token: string,
    newPassword: string
): Promise<void> => {
    await userRepository.confirmPasswordReset(email, token, newPassword, {
        fetch,
    });
};

// TODO full name should be optional
export async function updateUserProfile(
    fullName: string,
    repositoryContext: RepositoryContext
) {
    await updateUser({ full_name: fullName }, repositoryContext);
    // We fetch the user to make sure the full name is updated
    // Ideally, this would just store the result of the above operation
    // in the user store
    await fetchUser(repositoryContext);
}
